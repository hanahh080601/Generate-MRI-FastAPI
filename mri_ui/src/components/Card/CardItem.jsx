import React from 'react';
import './card.css';

export default function CardItem({ image_url, contrast }) {
    return (
        <div className="card-item">
            <img className='card-item-img' src={image_url + `&time=${new Date().getTime()}`} alt="mri_image"></img>
            <h2 className='card-item-txt'>{contrast}</h2>
        </div>
    )
}
