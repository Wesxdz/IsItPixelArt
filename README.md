## What is [pixel art](https://en.wikipedia.org/wiki/Pixel_art)?
<img src="https://pixeljoint.com/files/icons/full/catgameshowcase.gif">

I'm not sure, but I think [we know it when we see it](https://en.wikipedia.org/wiki/I_know_it_when_I_see_it).

Let's assume for now that any content <i>created natively by hand or procedural algorithm bounded within some arbitrarily low resolution square grid is ipso facto pixel art</i>.

Some of the earliest non pixel art games were created for [Nintendo 64](https://en.wikipedia.org/wiki/Nintendo_64), which has a resolution of 320×240. Therefore the prior platform, [NES](https://en.wikipedia.org/wiki/Nintendo_Entertainment_System) at 256x240 likely represents a cluster of pixel art approaching the boundry of non-pixel art.

<img src="https://www.mobygames.com/images/shots/l/433651-kirby-s-adventure-nes-screenshot-inside-a-museum-museums-keep.png">

* Low resolution images are not necessarily pixel art
* High resolution images can be pixel art: there is no upper limit
* 3D content can be pixel art
* What is considered pixel art may change over time in response to
    * new rendering techniques applied to retro artstyles
    * adoption of sensory devices that innovate in resolution, display qualia, or interaction mechanisms


#### Data
When I started this project, there were no [open datasets](https://en.wikipedia.org/wiki/List_of_datasets_for_machine-learning_research) available for machine learning on pixel art images.

How to collect a dataset of pixel art from the internet?

<table style="align:right;border:none;position:absolute;">
    <tr>
        <th>
           <img src="https://litreactor.com/sites/default/files/images/column/headers/drake_ignores_writing_advice.jpg">
       </th>
        <th width=50%>
            <ul float=left>
                <li><p>Images from <a href="https://twitter.com/search?q=%23pixelart">tweets tagged with #pixelart</p></a></li>
        </th>
    </tr>
    <tr>
        <th>
           <img src="https://i.kym-cdn.com/entries/icons/original/000/020/147/drake.jpg">
       </th>
        <th>
            <ul style="text-align:left">
                <li><a href="https://opengameart.org/art-search?keys=pixelart">Assets from OpenGameArt filtered by tag, art type, and license</a></li>
            <li><a href="https://www.spriters-resource.com/nes/">Spritesheets, tilesets</a>, or <a href="https://www.mobygames.com/info/standards#Screenshots">screenshots</a> from retro video games</li>
            <li>Pixel art communities like <a href="https://pixeljoint.com/">Pixel Joint</a></li>
            <ul>
        </th>
    </tr>
</table>

Manually cleanup data
* Mislabeled or unrelated data
* Redundancy (animations exported as series of individual images)
* False type indications (ie bmp named image.jpeg)
* Need an approach for animated images (using just the first frame is not viable, training on multiple frames per image complicates tensors)
   
Edge cases include
* Pixel art created in voxel games like Minecraft
* Upscaled pixel art composed together with non-pixel art textures such as in memes, marketing materials, and post-processing effects. More broadly some images consist of a dynamic mix, often this is expressed in UI. [Aseprite](https://www.aseprite.org/) is a anomalous example of a sprite editor which also renders its UI as pixel art.
* Photos of pixel art subtextures on surfaces including screens, stickers, and shirts; or composed of a material form like beads, LEGOs, etc...
* Non pixel art images scaled down with nearest neighbor
* Blurry, low-quality, or watermarked pixel art
* Non-standard scaling input like [Hqx](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms)
