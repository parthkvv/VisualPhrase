import React from "react";

class Select extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ""
        }
    }

    onChange = (event) => {
        this.setState({ value: event.target.value });
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.value !== this.state.value) {
            this.props.onChange(this.props.name, this.state.value);
        }
    }

    componentDidMount() {
        this.onChange({ target: { value: this.props.options[0] } });
    }


    render() {
        const { name, label, options } = this.props;
        return (
            <div>
                <label className="block text-sm font-medium text-gray-700">
                    {label}
                </label>
                <select name={name} value={this.state.value} onChange={this.onChange} className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    {options.map(value => {
                        return <option key={value}>{value}</option>
                    })}
                </select>
            </div>
        )
    }
}

export default Select;