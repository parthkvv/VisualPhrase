import React from 'react';
import Select from "./Select";

class AttentionHeadList extends React.Component {
    constructor(props) {
        super(props);
        let attentionNumHeads = this.props.num_heads;
        // var attentionHeadIndex = Array.apply(null, Array(5)).map(function (x, i) { return i; });
        this.state = {
            attentionHeadIndex: Array.apply(null, Array(attentionNumHeads)).map(function (x, i) { return i; })
        }
    }
    render() {
        
        //var attentionHeadIndex = Array.from({length: 5}, (v, i) => i)
        // let languageModel = this.props.languageModel
        // let cols = this.props.array[0].length;
        return (
            <>
                <Select label="Attention Head # (For Transformer)"
                    name="attentionhead"
                    options={this.state.attentionHeadIndex}
                    onChange={this.props.onChange}
                    />
            </>
        )
    }
}

export default AttentionHeadList;