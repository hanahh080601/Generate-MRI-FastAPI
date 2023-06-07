import React, { useState } from 'react';
import { ThreeCircles, RotatingLines, Puff, ThreeDots } from 'react-loader-spinner'

import axiosClient from "../services/http"
import Card from '../components/Card/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import InputFile from '../components/InputFile';
import InputSelection from '../components/SelectionBox';
import './style.css';

export default function Test() {
  const [sourceContract, setSourceContract] = useState('')
  const [targetContract, setTargetContract] = useState('')
  const [image, setImage] = useState(null)
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const [select, setSelect] = useState()
  console.log(select)

  const send = async () => {
    try {
      setIsLoading(true)
      setData(null)
      const res = await axiosClient.post("/generate/input_target_contrast", null, {
        params: { ["dataset"]: select, ["source_contrast"]: sourceContract, ["target_contrast"]: targetContract }
      })
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
      <h1 className='page-title'>Test page</h1>
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
        <InputSelection data={select} setData={setSelect} />

        <Button onClick={isLoading ? () => { } : send}>Generate</Button>

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
        <Card res={data} />
      )}
    </div>
  </>
}
