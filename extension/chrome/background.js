VISION_MODEL = "InceptionV3"
LANGUAGE_MODEL = "Transformer"
BASE_API_URL = "http://35.192.169.60.sslip.io/api"

function srcToFile(src) {
    return (fetch(src)
        .then(function (response) {
            return response.arrayBuffer();
        })
        .then(function (buffer) {
            return new File([buffer], 'image.jpg', { type: 'image/jpeg' });
        }));
}


async function post(endpoint, data) {
    const promise = fetch(BASE_API_URL + endpoint, {
        method: "POST",
        body: data,
    });
    const resp = await promise;
    return await resp.json();
}

async function process(file, endpoint) {
    var payload = {
        vision: VISION_MODEL,
        language: LANGUAGE_MODEL,
        image: file
    }

    let formData = new FormData();
    for (let [key, value] of Object.entries(payload)) {
        formData.append(key, value);
    }

    return await post(endpoint, formData).then(res => {
        return res.caption;
    });
}

// This is called when an image is clicked, makes the API call, and returns the caption to eh content script
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.msg === 'image') {
        srcToFile(message.image).then(file => {
            process(file, "/predict").then(res => {
                sendResponse([res, null]);
            }).catch(err => {
                sendResponse([null, err]);
            });
        }).catch(err => {
            sendResponse([null, err]);
        });
    }
    return true;
});
