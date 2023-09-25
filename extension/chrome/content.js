// Populates the alt text with a caption when the user clicks on an image
// let imgs = document.getElementsByTagName("img");
// for(let i = 0; i < imgs.length; ++i) {
//     imgs[i].addEventListener("click", function() {
//         //alert(this.src);
//         if (!this.alt) {
//             chrome.runtime.sendMessage({ msg: "image", image: this.src }, response => {
//                 if (response === null) {
//                     console.log(error);
//                 } else {
//                     this.alt = response;
//                 }
//             });
//         }
//     });
// }
// Access to the whole page and all images at once

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processPage);
} else {
    processPage();
}

function processPage() {
    let images = document.getElementsByTagName("img");
    for (let i = 0; i < images.length; i++) {
        let image = images[i];
        if (!image.alt) {
            chrome.runtime.sendMessage({ msg: "image", image: image.src }, response => {
                if (response === null) {
                    console.log("error generating alt text");
                } else {
                    console.log(i, response);
                    image.alt = response;
                }
            });
        }
    }
}