import UploadPage from "../pages/UploadPage"
import InputContrast from "../pages/InputContrast"
import ChooseModel from "../pages/ChooseModel"
import UploadOuterImage from "../pages/UploadOuterImage"

export const appRoutes = [
    { path: "/upload_page", component: UploadPage },
    { path: "/input_page", component: InputContrast },
    { path: "/choose_model", component: ChooseModel },
    { path: "/outer_image", component: UploadOuterImage },

]