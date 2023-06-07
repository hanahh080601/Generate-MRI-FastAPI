import "./style.sass";
import { useState } from "react";

export default function InputSelection({ data, setData }) {
    const handleChange = (e) => {
        if (data !== e.target.value) {
            setData(e.target.value)
        }
    }

    return (
        <div className="select animated zoomIn">
            <input type="radio" name="option" />
            <i className="toggle icon icon-arrow-down"></i>
            <i className="toggle icon icon-arrow-up"></i>
            <span className="placeholder">Choose dataset...</span>
            <label className="option">
                <input type="radio" name="option" className="option-input" value="IXI" onChange={handleChange} />
                <span className="title animated fadeIn">IXI</span>
            </label>
            <label className="option">
                <input type="radio" name="option" className="option-input" value="BraTS2020" onChange={handleChange} />
                <span className="title animated fadeIn">BraTS2020</span>
            </label>
        </div>
    )
}
