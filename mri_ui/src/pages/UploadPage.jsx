import React, { useState } from 'react';
import { ThreeCircles, RotatingLines, Puff, ThreeDots } from 'react-loader-spinner'

import axiosClient from "../services/http"
import Card from '../components/Card/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import InputFile from '../components/InputFile';
import InputSelection from '../components/SelectionBox';
import Metrics from '../components/Metrics';
import './style.css';

export default function Test() {
    const [sourceContract, setSourceContract] = useState('')
    const [targetContract, setTargetContract] = useState('')
    const [image, setImage] = useState(null)
    const [data, setData] = useState(null)
    const [isLoading, setIsLoading] = useState(false)

    const [select, setSelect] = useState()
    console.log(select)

    const sendFile = async () => {
        try {
            setIsLoading(true)
            setData(null)
            const formData = new FormData()
            formData.append("file", image)
            const res = await axiosClient.post(
                "/generate/uploaded_file",
                formData,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                    params: {
                        ["dataset"]: select,
                        ["src_contrast"]: sourceContract,
                        ["trg_contrast"]: targetContract
                    }
                }
            )
            console.log(res)
            if (res) {
                setData(res)
            }
        } catch (err) {
            console.log(err)
        } finally {
            setIsLoading(false)
        }
    }

    return <>
        <div className='page-container'>
            <h1 className='page-title'>MRI SYNTHESIS</h1>
            <div className="input-form-container">
                <Input
                    name="source_contrast"
                    placeholder="Source Contrast"
                    value={sourceContract}
                    setValue={setSourceContract} />
                <Input
                    name="target_contrast"
                    placeholder="Target Contrast"
                    value={targetContract}
                    setValue={setTargetContract} />
                <InputSelection
                    label="dataset"
                    name="dataset"
                    data={select}
                    setData={setSelect}
                    options={[{ value: 'IXI', label: 'IXI' }, { value: 'BraTS2020', label: 'BraTS2020' }]}
                />

                <InputFile image={image} setImage={setImage} name="file" />
                <Button onClick={isLoading ? () => { } : sendFile}>Generate</Button>

            </div>
            <Puff
                height="100"
                width="100"
                radius={1}
                color="#ffc8c8c4"
                ariaLabel="puff-loading"
                visible={isLoading}
                wrapperStyle={{
                    padding: 150,
                }}
            />
            {!!data && (
                <>
                    <Metrics res={data} />
                    <Card res={data} />
                </>
            )}
        </div>
    </>
}
