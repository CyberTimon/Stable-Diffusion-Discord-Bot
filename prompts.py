def make_prompt(prompt, style, original_negativeprompt):
    if style == 'No Style Preset':
        preprompt = ""
        afterprompt = ""
        negativeprompt_template = "monochrome, nsfw, nude, borders, low quality, low resolution, greyscale"
    elif style == 'Low Poly':
        preprompt = "A low poly image of a " 
        afterprompt = ", low poly, soft lighting, cute, masterpiece, (best quality), polygon, trending on artstation, sharp focus, low poly model, render, 4k, flat colors"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, realistic, watermarks, text, signature"
    elif style == 'Anime':
        preprompt = "An picture of a "
        afterprompt = ", anime style, masterpiece, (best quality), fantasy, trending on artstation, anime-style, bokeh, dreamlike, concept art, hyperrealism, color digital painting, anime aesthetic, cinematic lighting, trending pixiv, by Brad Rigney and greg rutkowski makoto shinkai takashi takeuchi studio ghibli"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, border, old, deformed iris, deformed pupils, out of frame, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, nsfw, extra legs, frame, borders, fused fingers, too many fingers, long neck, raw, drops, particles, watermarks, text, signature"
    elif style == 'Oilpainting':
        preprompt = "Oil painting of a "
        afterprompt = ", oil painting, colors, art, ink, drawing, oil brushstrokes, abstract, paint textures, by Leonid Afremov and Brad Rigney"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, nsfw, watermarks, text, signature"
    elif style == 'Cute':
        preprompt = "Cute image of a "
        afterprompt = ", fantasy, miniature, soft lighting, flat colors, dreamlike, small, surrealism, bokeh, unreal engine, trending on artstation"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, realistic, nsfw, dark, reallife, texture, realistic, raw"
    elif style == 'Comic':
        preprompt = "Retro comic style artwork, a "
        afterprompt = ", comic, anime style, 1970's, vibrant"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, nsfw, realistic, raw, watermarks, text, signature"
    elif style == 'Cyberpunk':
        preprompt = "A picture of a "
        afterprompt = ", futuristic, lights, high quality, cyberpunk, octane render, greg rutkowski, highly detailed, trending on artstation, volumetric lighting, dynamic lighting"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, human, nsfw, watermarks, text, signature"
    elif style == 'Steampunk':
        preprompt = "A digital illustration of a steampunk "
        afterprompt = ", clockwork machines, 4k, detailed, trending in artstation, mechanism, metal, pipes, fantasy vivid colors, sharp focus"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, realistic, raw, human, watermarks, text, signature"
    elif style == 'Vintage':
        preprompt = "Vintage 1950s illustration poster of a "
        afterprompt = ", low contrast, vintage, 1950, old fashion, illustration, vector, flat colors, flat design"
        negativeprompt_template = "ugly, realistic, raw, text, title, borders, colorful, description, nsfw, watermarks, text, signature"
    elif style == 'Apocalyptic':
        preprompt = "A apocalyptic picture of a "
        afterprompt = ", distopic, cinestill, photography, scary, foggy, ruin, realistic, hyper detailed, unreal engine, cinematic, octane render, lights, greg rutkowski"
        negativeprompt_template = "ugly, realistic, raw, text, title, colorful, description, watermarks, text, signature"
    elif style == 'Natural':
        preprompt = "RAW photo of a "
        afterprompt = ", dslr, soft lighting, intricate details, sharp focus, 8k, 4k, UHD, raw, Fujifilm XT3"
        negativeprompt_template = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, bokeh, ugly, duplicate, fat, old, aged, fat, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, 480p, 360p, poorly drawn face, camera, nude, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, watermarks, text, signature"
    elif style == 'Watercolor':
        preprompt = "A watercolor painting of a "
        afterprompt = ", detailed line art, color explosion, ink drips, art, watercolors, wet, single color, abstract, by ilya kuvshinov"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, human, woman, realistic, anime, japan, nsfw, watermarks, text, signature"
    elif style == 'Fantasy':
        preprompt = "Digital concept art of a "
        afterprompt = ", masterpiece, (best quality), fantasy, volumetric lighting, trending on artstation, dreamlike, concept art, hyperrealism, color digital painting, aesthetic, cinematic lighting, 4k, 8k, trending pixiv, by greg rutkowski"
        negativeprompt_template = "Bad, low quality, worst quality, ugly, old, human, nsfw, watermarks, text, signature"
    elif style == 'Cinematic':
        preprompt = "RAW cinematic picture of a "
        afterprompt = ", cinematic look, cinematic, best quality, perfect focus, color grading, 70mm lens, lightroom, 8k, 4k, UHD, Nikon Z FX, sharp focus, Fujifilm XT3, (rutkowski:1.1), artstation, HDR, greg rutkowski"
        negativeprompt_template = "(deformed iris, nsfw, barely clothed, naked, deformed pupils, borders, frame, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, nude, nsfw, borders, cropped, out of frame, worst quality, low quality, low resolution, 480p, jpeg artifacts, ugly, duplicate, fat, old, aged, fat, morbid, mutilated, extra fingers, camera, border, mutated hands, poorly drawn hands, poorly drawn face, nude, mutation, nsfw, deformed, blurry, skin, dehydrated, bad anatomy, 480p, 360p, bad proportions, extra limbs, bad focus, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, watermarks, text, signature"
    else:
        preprompt = ""
        afterprompt = ""
        negativeprompt_template = "monochrome, nsfw, nude, borders, low quality, low resolution, greyscale"
        
    prompt = preprompt + prompt + afterprompt
    negativeprompt = original_negativeprompt + ", " + negativeprompt_template
    return prompt, negativeprompt

def make_orientation(orientation):
    if 'Landscape' in orientation:
        width = 683
        height = 512
    elif 'Portrait' in orientation:
        width = 512
        height = 683
    elif 'Square' in orientation:
        width = 512
        height = 512
    else:
        width = 512
        height = 512
    return width, height