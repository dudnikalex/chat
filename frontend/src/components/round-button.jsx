import React from 'react';
import './components.scss';

const RoundButton = (props) => {
    const bgColor = props.color ? props.color : '#5d22dc';
    return (
        <button
            style={{ 'backgroundColor': bgColor }}
            onClick={props.onClick}
            className="round-button">
            {props.children}
        </button>
    );
};

export default RoundButton;
