MENU_COMMANDS = {
    '/start': 'Start',
    '/upload_style': 'Upload an photo to use as a style',
    '/upload_content': 'Upload an photo to use as a content',
    '/default_photos': 'Set the default style and content',
    '/transfer': 'Transfer the style of one photo to another',
    '/set_parameters': "Set the network's parameters",
    '/cancel': 'Cancel the process',
    '/help': 'Get bot help'
}

CMD_ANSWER = {
    'start': 'This bot blends the style of one photo with another!\n'
             'Use commands to customize and start the magic!\n'
             'Need a guide? Type "/help" for a detailed list of commands',
    'help': '/upload_style:\tTo apply a specific style to your conten '
            'image, send a photo with this caption or '
            'simply type this command and follow it '
            'with the photo in the next message.\n'
            '/upload_content:\tSend the photo which style you want '
            'to update with this caption, or '
            'simply type this command and follow it '
            'with the photo in the next message.\n'
            '/default_photos:\tUse this command to apply default style '
            'and content photos for the transformation.\n'
            '/transfer:\tInitiate the model training process to '
            'transfer the style of one image to another\n'
            '/set_parameters:\tCustomize the number of training epochs and '
            'style resolution. The default values are '
            '300 epochs and medium resolution.\n'
            '/cancel:\tTo terminate the upload_style,\n'
            'upload_content, or transfer '
            'simply type this command',
    'set_default_photos': 'The photos above were set as style '
                          'and content, respectively.',
    'upload_style_success': 'The photo style has been uploaded.',
    'upload_style_instruction': 'Send the photo in your next message.',
    'upload_content_success': 'The photo content has been uploaded.',
    'upload_content_instruction': 'Send the photo in your next message.',
    'transter_waiting_photos': 'Upload photos with the /upload_content '
                               'and /upload_style commands. Alternatively, '
                               'you can use the /default_photos command.',
    'transter_waiting_content': 'Upload the content photo with the'
                                '/upload_content command. Alternatively, '
                                'you can use the /default_photos command.',
    'transter_waiting_style': 'Upload the style photo with the '
                              '/upload_content command. Alternatively, '
                              'you can use the /default_photos command.',
    'starting_transferring': 'The style transfer has begun using the '
                            'style and content photos provided above',
    'transferring_succses': 'Style transfer is complete!',
    'transferring_fail': 'The transfer is failing. Try lowering the '
                        'resolution or reducing the number of epochs',
    'cancel_transferring_succuses': 'The transfer has been terminated.',
    'cancel_photo_upload': 'The photo upload has been terminated.'
}

SET_PARAMS_KB = {
    'set_epoch': 'Set epochs number',
    'set_resolution': 'Set photo resolution',
    'cancel_keyboard': 'Cancel',
}

SET_EPOCH_KB = {
    'epoch100': '100',
    'epoch300': '300',
    'epoch500': '500',
    'back_2setparams': 'Back',
    'cancel_keyboard': 'Cancel'
}

SET_RESOLUTION_KB = {
    'resolution_small': 'SMALL',
    'resolution_middle': 'MIDDLE',
    'resolution_large': 'LARGE',
    'back_2setparams': 'Back',
    'cancel_keyboard': 'Cancel'
}
