import {useEffect, useState} from "react"

import "./styles.css";

export default function InputFile({ image, setImage, name }) {
    const [preview, setPreview] = useState()

    useEffect(() => {
        if (!image) {
            setPreview(undefined)
            return
        }
        const url = URL.createObjectURL(image)
        // setPreview(url)
        return () => URL.revokeObjectURL(url)
    }, [image])

    const onChange = (e) => {
        if (!e.target.files || e.target.files.length === 0) {
            setImage(undefined)
            return
        }
        setImage(e.target.files[0])
    }

    return (
        <>
            <input
                className="file-input"
                type="file"
                accept="image/*"
                name={name}
                onChange={onChange}
            />
            {(image && preview) && <img src={preview} alt="preview" className="image-preview" />}
        </>
    );
}
