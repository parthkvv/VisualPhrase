import React from "react"
import Loader from "./Loader";

function Caption(props) {
    let { caption, onWordHover } = props;
    let { status, text } = caption;

    return (
        <div className="text-md leading-6 text-gray-900">
            <div>
                {
                    (() => {
                        switch (status) {
                            case "processing":
                                return <Loader text="Processing..." />;
                            case "success":
                                return <h3><span className="mr-1">Caption:</span>
                                    {
                                        text.split(" ").map((word, index) => {
                                            return (
                                                <span key={index} onMouseOver={() => onWordHover(index)} onMouseOut={() => onWordHover(null)} className="mr-1 cursor-pointer hover:text-gray-500">
                                                    {word}
                                                </span>
                                            );
                                        })
                                    }
                                </h3>;
                            case "error":
                                return <h3>There was an error creating the caption.</h3>;
                            default:
                                return "";
                        }
                    })()
                }
            </div>
        </div>
    )
}

export default Caption;