# MRI Synthesis Using Deep Learning Models (Pytorch, FastAPI & ReactJS)

## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/hanahh080601/Generate-MRI-FastAPI
git checkout hanlhn/update_api
git pull
# Back-end
cd generate_mri_fastapi
poetry install
poetry config virtualenvs.in-project true

# Front-end
yarn install
```

## Usage: 
```bash
# Back-end
cd generate_mri_fastapi
. .venv/bin/activate
cd generate_mri_fastapi
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Front-end
cd mri_ui
yarn start
```

## Link to website
http://hanlhn8601.tech/

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 
