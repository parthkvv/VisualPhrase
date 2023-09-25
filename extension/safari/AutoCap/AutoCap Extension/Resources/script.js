// async function processPage() {
//     var images = document.images;
//     var imagesLength = images.length;

//     for (let i = 0; i < imagesLength; i++) {
//         let image = images[i];
//         // console.log(image, i);
//         if (!image.alt) {
//             const text = await srcToFile(images[i].src).then(file => {
//                 process(file).then(res => {
//                     console.log(res);
//                     image.alt = res;
//                 });
//             });
//         }
//     }
// }

// document.addEventListener("DOMContentLoaded", function (event) {
//     processPage();
// });
