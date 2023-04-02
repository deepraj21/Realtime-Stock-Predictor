import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import moment from "moment";
import predict from "./api/predict";

const Chart = () => {
    const [data, setData] = useState({});
    const [ticker, setTicker] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            const predictedData = await predict(ticker);
            setData({
                labels: predictedData.map((d) => moment(d.date).format("DD/MM/YYYY")),
                datasets: [
                    {
                        label: "Predicted Prices",
                        data: predictedData.map((d) => d.price),
                        fill: false,
                        borderColor: "#0F52BA",
                    },
                ],
            });
        };
        fetchData();
    }, [ticker]);

    const handleInputChange = (event) => {
        setTicker(event.target.value.toUpperCase());
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
    };

    return (
        <div>
            <input type="text" onChange={handleInputChange} />
            <Line data={data} options={options} />
        </div>
    );
};

export default Chart;
