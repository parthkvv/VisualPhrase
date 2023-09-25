# API and React Frontend - Local Development

## Flask API
- `cd api`
- `mkdir models`
- Download all models from [Google Drive](https://drive.google.com/drive/u/0/folders/1Fmduznf6Agnyt2Jx2D1l0YqqghqvOG0b) and place them within this newly created `models` folder.

- Run `sh docker-shell.sh`

This will run the api on port 5001 of your local machine.

## React Frontend
- `cd frontend`
- Run `sh docker-shell-dev.sh`

This runs the React app on port 3000. Navigate to `http://localhost:3000` in your browser to view the app. In this development environment, React defines the API url to be `http://localhost:5001`. In production, the API url is `/api`, which will be created and handled appropriately by nginx.

To test the production React app, run `sh docker-shell.sh`. Note that since we did not also create an nginx reverse proxy locally, the API will not work in this context.