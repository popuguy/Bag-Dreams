## Bag Dreams with GANs in PyTorch

In the final week of this quarter, I worked to try interacting with and making generative adversarial neural nets (GANs). Video summary [here](www.youtube.com).

### Acquiring data

Typical student and professional neural net projects seem to rely on massive, clean, labeled datasets that can practically not be created without a large amount of time or funding. To subvert this model for projects and make something slightly more unique, I worked to create a GAN with data I could find online.

The first stage of work on my project consisted of finding and downloading a stockpile of images in my area of interest. I'm interested in bags and have been [making bags](https://heavycreambags.com/) for a couple years, so I was curious to try to create a network that could also "design" bags. To my knowledge, the best troves of clean bag images are on retail luxury consignment websites like [The RealReal](https://www.therealreal.com/) and [Rebag](https://www.rebag.com/).

My scripts for compiling images with some tagged data for possible use in later networks use a combination of the Python Selenium and BeautifulSoup libraries to achieve a total supply of over 38,000 images. I have a separate script for squaring images with proper whitespace and downsizing to an appropriate resolution for training on my graphics card.

### Methods

My network is a traditional GAN that I reasoned through the creation of by closely looking through a few different projects as references. The adversarial model is one where there are really two separate component networks that learn together as if playing a game. These two components are called the "Generator" and the "Discriminator."

For my network, my generator uses layers of transposed convolution operations to scale up from 128 randomly generated values to a 3-channel (full color) 64x64 image to perform the forward pass, generating the image. The discriminator is then posed against the generator by using spaced strides in convolution operations to scale back to a single output value representing an interpretation of the image as real or fake. The discriminator is trained at each iteration through a batch of real images and these generated fakes. As the discriminator performs its backward pass, it also passes back blame to the generator so it, in turn, can learn.

### Results
<img src="https://github.com/popuguy/Bag-Dreams/blob/main/dreamed-bags/present/some-bags.jpg?raw=true" alt="hi" />
Although the generator learns from random inputs during training, I can track a number of these randomly generated values as a seed to examine network progress. As depicted in my video summary, the change in outputs for given seeds over time can be somewhat mesmerizing as well as informative for the true test of a convincing look for a human observer.



## References

https://github.com/nbertagnolli/pytorch-simple-gan
https://github.com/eriklindernoren/PyTorch-GAN/
https://sthalles.github.io/advanced_gans/
https://www.kaggle.com/spandan2/cats-faces-64x64-for-generative-models
https://machinelearningmastery.com/how-to-develop-a-pix2pix-gan-for-image-to-image-translation/
