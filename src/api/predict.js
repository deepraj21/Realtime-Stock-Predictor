import axios from "axios";

const BASE_URL = "http://localhost:5000";

const predict = async (ticker) => {
    const response = await axios.post(`${BASE_URL}/predict`, { ticker });
    return response.data;
};

export default predict;
