import "./style.sass";
import { useState } from "react";

export default function InputSelection({ data, setData, options, label, name }) {
    const handleChange = (e) => {
        if (data !== e.target.value) {
            setData(e.target.value)
        }
    }

    return (
        <div className="select animated zoomIn">
            <input type="radio" name={name} />
            <i className="toggle icon icon-arrow-down"></i>
            <i className="toggle icon icon-arrow-up"></i>
            <span className="placeholder">Choose {label}...</span>
            {Array.from(options).map((option) => (
                <label className="option">
                    <input type="radio" name={name} className="option-input" value={option.value} onChange={handleChange} />
                    <span className="title animated fadeIn">{option.label}</span>
                </label>
            ))}
        </div>
    )
}
