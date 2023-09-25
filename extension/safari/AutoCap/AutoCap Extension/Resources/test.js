// document.addEventListener("DOMContentLoaded", function (event) {
//     let images = Array.from(document.images);
//     images.forEach(function (image, index) {
//         if (!image.alt) {
//             safari.extension.dispatchMessage("passImage", { "index": index, "image": image.src})
//         }
//     });
// });

// function handleResponse(event) {
//     // let image = document.images[event.message.index];
//     // let caption = event.message.image;
//     // image.alt = caption;
//     console.log(event);
    
// }

// safari.self.addEventListener("message", handleResponse);

browser.runtime.sendNativeMessage("application.id", {message: "Hello from background page"}, function(response) {
    console.log("Received sendNativeMessage response:");
    console.log(response);
});