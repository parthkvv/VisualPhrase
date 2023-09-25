import React from "react";
import Loader from "./Loader";
import Select from "./Select";
import { get } from "../actions/requests";

class Settings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            availableModels: {
                vision: null,
                language: null
            },
            loaded: false
        }
    }

    componentDidMount() {
        get('/models').then(res => {
            var vision = res.vision;
            var language = res.language;
            this.setState({
                availableModels: {
                    vision: vision,
                    language: language
                },
                loaded: true
            });
        });
    }

    render() {
        if (this.state.loaded) {
            return (
                <>
                    <div>
                        <h3 className="text-lg font-medium leading-6 text-gray-900">
                            Settings
                        </h3>
                        <p className="mt-1 text-sm text-gray-900 mb-4">
                            Change image captioning model pipeline.
                        </p>
                    </div>
                    <Select label="Vision model"
                        name="vision"
                        options={this.state.availableModels.vision}
                        onChange={this.props.onChange}
                    />
                    <Select label="Language model"
                        name="language"
                        options={this.state.availableModels.language}
                        onChange={this.props.onChange}
                    />
                </>
            );
        }
        else {
            return (
                <div>
                    <h3 className="text-lg font-medium leading-6 text-gray-900">
                        Settings
                    </h3>
                    <Loader text="Loading models..." />
                </div>
            );
        }
    }
}

export default Settings;