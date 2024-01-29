import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules import Sequential


class ContentLoss(nn.Module):

    def __init__(self, target: torch.FloatTensor):
        super(ContentLoss, self).__init__()
        self.target = target.detach()

    def forward(self, input: torch.FloatTensor):
        self.loss = F.mse_loss(input, self.target)
        return input


class StyleLoss(nn.Module):
    @staticmethod
    def gram_matrix(input: torch.FloatTensor):
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)
        G = torch.mm(features, features.t())
        return G.div(a*b*c*d)

    def __init__(self, target: torch.FloatTensor):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target).detach()

    def forward(self, input: torch.FloatTensor):
        G = self.gram_matrix(input)
        self.loss = F.mse_loss(G, self.target)
        return input


class Normalization(nn.Module):

    def __init__(self, mean: torch.Tensor, std: torch.Tensor):
        super(Normalization, self).__init__()
        self.mean = mean.view(-1, 1, 1)
        self.std = std.view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std


def build_model(
        base_cnn: Sequential,
        content_img: torch.FloatTensor, style_img: torch.FloatTensor,
        norm_mean: torch.Tensor = torch.tensor([0.485, 0.456, 0.406]),
        norm_std: torch.Tensor = torch.tensor([0.229, 0.224, 0.225]),
        content_layers: list[str] = ['conv_4'],
        style_layers: list['str'] = ['conv_1', 'conv_2', 'conv_3',
                                     'conv_4', 'conv_5']
):
    content_losses = []
    style_losses = []

    model = nn.Sequential(
        Normalization(norm_mean, norm_std)
    )
    target = model(style_img)
    i = 0
    for layer in base_cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = f'conv_{i}'
        elif isinstance(layer, nn.ReLU):
            name = f'relu_{i}'
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = f'maxpool_{i}'
        elif isinstance(layer, nn.BatchNorm2d):
            name = f'batchnorm_{i}'
        else:
            raise RuntimeError(f'Wrong layer: {layer.__class__.__name__}')
        model.add_module(name, layer)
        if name in content_layers:
            target = model(content_img)
            content_loss = ContentLoss(target)
            model.add_module(f'content_loss_{i}', content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target = model(style_img)
            style_loss = StyleLoss(target)
            model.add_module(f'style_loss_{i}', style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) \
           or isinstance(model[i], StyleLoss):
            break
    model = model[:i+1]
    return model, style_losses, content_losses
