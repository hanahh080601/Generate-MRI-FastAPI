import React from 'react'
import './style.css'

export default function Metrics({ res }) {
    const { nmae, psnr, ssim } = res
    return <div className='card-container'>
        <span className='metric-item'>
            <span className='metric-label'>NMAE </span>
            <span className='metric-data'>{(+nmae).toFixed(5)}</span>
        </span>
        <span className='metric-item'>
            <span className='metric-label'>PSNR </span>
            <span className='metric-data'>{(+psnr).toFixed(5)}</span>
        </span>
        <span className='metric-item'>
            <span className='metric-label'>SSIM </span>
            <span className='metric-data'>{(+ssim).toFixed(5)}</span>
        </span>
    </div>
}
