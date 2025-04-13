import "./Pricing.scss";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import VideoItem from "./VideoItem";
import AnimationVariants from "../AnimationVariants/AnimationVariants";

const Pricing = () => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  const videoData = [
    {
      id: 1,
      title:
        "TOP 5 SŁUCHAWEK GAMINGOWYCH DO 150/200/300ZŁ | Najlepsze słuchawki [2021]",
      url: "https://www.youtube.com/watch?v=EZagYbsGJeU",
      thumbnail: "https://img.youtube.com/vi/EZagYbsGJeU/maxresdefault.jpg",
    },
    {
      id: 2,
      title:
        "TOP 5 KLAWIATUR GAMINGOWYCH DO 200ZŁ | Najlepsze klawiatury [2021]",
      url: "https://www.youtube.com/watch?v=uuKotb4_GxI",
      thumbnail: "https://img.youtube.com/vi/uuKotb4_GxI/maxresdefault.jpg",
    },
    {
      id: 3,
      title: "TOP 5 MYSZEK GAMINGOWYCH DO 100ZŁ | Najlepsze myszki [2021]",
      url: "https://www.youtube.com/watch?v=4pzPTtDGz3c",
      thumbnail: "https://img.youtube.com/vi/4pzPTtDGz3c/maxresdefault.jpg",
    },
  ];

  return (
    <motion.section
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}
      className="pricing">
      <h2 className="pricing__title">Watch Our Latest Reviews</h2>
      <p className="pricing__subtitle">
        Check out our top gaming gear reviews. Find the best products in the
        market.
      </p>
      <div className="pricing__container">
        {videoData.map((video) => (
          <VideoItem key={video.id} {...video} />
        ))}
      </div>
    </motion.section>
  );
};

export default Pricing;
