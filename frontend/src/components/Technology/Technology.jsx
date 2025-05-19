import AboutContent from "../AboutContent/AboutContent";
import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import techImage from "../../assets/tech.webp";

const TechOverview = () => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  return (
    <motion.div
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}>
      <AboutContent
        img={techImage}
        alt="Modern technology setup"
        title="Technology Is the Answer..."
        span="WHEN THE QUESTION IS YOUR HARDWARE NEEDS!"
        text="Based on the principle that proper technology selection is key to effective use, we've created a platform utilizing advanced recommendation algorithms. Whether you're looking for efficient work equipment, high-end gaming setups, or business solutions, our system analyzes your preferences to deliver personalized recommendations tailored to your requirements."
        showIcons={false}
      />
    </motion.div>
  );
};

export default TechOverview;
