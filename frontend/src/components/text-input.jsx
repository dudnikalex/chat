import React from 'react';
import './components.scss';

export default class TextInput extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            text: '',
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        this.props.onSubmit(this.state.text);
    }

    onChange(event) {
        this.setState({
            text: event.target.value,
        });
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input
                    type="text"
                    onChange={this.onChange}
                    value={this.state.text}
                    className="input"></input>
                <input type="submit" style={{ display: 'none' }} />
            </form>
        );
    }
}
