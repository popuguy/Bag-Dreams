## Bag Dreams with GANs in PyTorch

In the final week of this quarter, I worked to try interacting with and making generative adversarial neural nets (GANs).

### Acquiring data

Typical student and professional neural net projects seem to rely on massive, clean, labeled datasets that can practically not be created without a large amount of time or funding. To subvert this model for projects and make something slightly more unique, I worked to create a GAN with data I could find online.

The first stage of work on my project consisted of finding and downloading a stockpile of images in my area of interest. I'm interested in bags and have been [making bags](https://heavycreambags.com/) for a couple years, so I was curious to try to create a network that could also "design" bags. To my knowledge, the best troves of clean bag images are on retail luxury consignment websites like [The RealReal](https://www.therealreal.com/) and [Rebag](https://www.rebag.com/).

My scripts for compiling images with some tagged data for possible use in later networks use a combination of the Python Selenium and BeautifulSoup libraries to achieve a total supply of over 38,000 images. I have a separate script for squaring images with proper whitespace and downsizing to an appropriate resolution for training on my graphics card.

### Methods

My network is a traditional GAN that I reasoned through the creation of by closely looking through a few different projects as references. The adversarial model is one where there are really two separate component networks that learn together as if playing a game. These two components are called the "Generator" and the "Discriminator."

For my network, my generator uses layers of transposed convolution operations to scale up from 128 randomly generated values to a 3-channel (full color) 64x64 image to perform the forward pass, generating the image. The discriminator is then posed against the generator by using spaced strides in convolution operations to scale back to a single output value representing an interpretation of the image as real or fake. The discriminator is trained at each iteration through a batch of real images and these generated fakes. As the discriminator performs its backward pass, it also passes back blame to the generator so it, in turn, can learn.

### Results

Although the generator learns from random inputs during training, I can track a number of these randomly generated values as a seed to examine network progress. <img src="https://ssl.gstatic.com/ui/v1/icons/mail/rfr/logo_gmail_lockup_default_1x_r2.png" alt="hi" class="inline"/>


```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/popuguy/Bag-Dreams/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.

## References

https://github.com/nbertagnolli/pytorch-simple-gan
https://github.com/eriklindernoren/PyTorch-GAN/
https://sthalles.github.io/advanced_gans/
