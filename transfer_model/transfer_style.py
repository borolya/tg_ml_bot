import torch
from torch.optim.lbfgs import LBFGS
import torch.optim as optim
import torchvision.transforms as transforms
from torch.nn.modules import Sequential
from torchvision.models import vgg19, VGG19_Weights
from torchvision.transforms.functional import to_pil_image
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from aiogram.types.input_media_photo import InputMediaPhoto
from PIL.Image import Image as ImageType
import logging
import io

from transfer_model.model_builder import build_model, StyleLoss, ContentLoss
from FSM.fsm import FSMState

logger = logging.getLogger(__name__)


def tensor_2bufferedfile(img: torch.FloatTensor):
    pil_img = to_pil_image(img)
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')
    img_byte_byte = img_byte_arr.getvalue()
    return BufferedInputFile(img_byte_byte, filename='buffile')


def image_process(img: torch.FloatTensor, size: int):
    loader = transforms.Compose([
        transforms.Resize([size, size]),
        transforms.ToTensor()
    ])
    img = loader(img).unsqueeze(0)
    return img


def img_postprocess(img: torch.FloatTensor,
                    size: tuple[int, int] | None = None):
    if not torch.is_tensor(img):
        raise TypeError(f'Wrong {type(img)} type, expected torch.tensor')
    if size is not None:
        transform = transforms.Resize(size, antialias=True)
    img = transform(torch.squeeze(img))
    return img


async def send_photo(msg: Message, bot: Bot, chat_id: int,
                     photo: torch.FloatTensor, epoch: int | None = None,
                     final: bool = False):

    buf_photo = tensor_2bufferedfile(photo)

    if final:
        caption = f'Final photo with last epoch={epoch}'
    else:
        caption = f'transfering in progress, epoch={epoch}'
    msg = await bot.edit_message_media(
        chat_id=chat_id,
        message_id=msg.message_id,
        media=InputMediaPhoto(media=buf_photo,
                              caption=caption)
    )
    return msg


async def training(input_img: torch.FloatTensor, model: Sequential,
                   optimizer: LBFGS, style_losses: list[StyleLoss],
                   content_losses: list[ContentLoss], msg: Message,
                   bot: Bot, chat_id: int, fsm_state: FSMContext,
                   size=None, epochs: int = 100, style_weight: int = 100000,
                   content_weight: int = 1):
    input_img.requires_grad_(True)
    model.requires_grad_(False)
    model.eval()
    final = False
    epoch = [0]
    while epoch[0] < epochs+1:
        # get fsm_state to stop in case of /cancel telegram command
        current_state = await fsm_state.get_state()
        logging.info(f'fsm_state={current_state}, epoch={epoch[0]}')
        if current_state != FSMState.transfer_style:
            logging.info(f'STOP TRAINING, epoch={epoch[0]}')
            break

        # to update photo in telegram during trainig
        if size is not None:
            with torch.no_grad():
                input_img.clamp_(0, 1)
                img = img_postprocess(input_img, size)
                msg = await send_photo(msg, bot, chat_id, img, epoch[0],
                                       final=(epoch[0] == epochs))
                logger.debug(f'New msg = {msg}')

        def closure():
            with torch.no_grad():
                input_img.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_img)

            style_score = 0
            content_score = 0

            for loss in style_losses:
                style_score += loss.loss
            for loss in content_losses:
                content_score += loss.loss

            loss = style_score*style_weight + content_score*content_weight
            loss.backward()

            if epoch[0] % 50 == 0:
                logger.info(f'Epoch={epoch[0]}')
                logger.info(f'style_loss={style_score*style_weight}\t'
                            f'content_loss={content_score*content_weight}')
            epoch[0] += 1
            return loss

        optimizer.step(closure)

    with torch.no_grad():
        input_img.clamp_(0, 1)
    return input_img, msg, epoch[0]


async def net_transfer_style(
        style_img: ImageType, content_img: ImageType,
        size: int, epochs: int, chat_id: int,
        bot: Bot, fsm_state: FSMContext, last_msg: Message):

    # set torch device
    device = torch.device('cude' if torch.cuda.is_available() else "cpu")
    torch.set_default_device(device)
    logger.info(f'device is {device}')

    # images preprocessing
    style_img = image_process(style_img, size).to(device)
    content_shape = (content_img.size[1], content_img.size[0])
    content_img = image_process(content_img, size).to(device)
    # model building. taking base like vgg19 from torch
    cnn = vgg19(weights=VGG19_Weights.DEFAULT).features.eval()
    model, style_losses, content_losses = build_model(cnn, content_img,
                                                      style_img)

    # set content image like starting point for network training
    input_img = content_img.clone()
    # alternative way is white noise
    # input_img = torch.randn(content_img.data.size())

    # starting network training
    optimizer = optim.LBFGS([input_img])
    output, msg, final_epoch = await training(
        input_img, model, optimizer, style_losses,
        content_losses, size=content_shape, epochs=epochs,
        msg=last_msg, bot=bot, chat_id=chat_id,
        fsm_state=fsm_state
    )
    # final photo update
    #output = img_postprocess(output, content_shape)
    #await send_photo(msg, bot, chat_id, output, final_epoch, final=True)
    return output
