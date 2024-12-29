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
        title="Technology is the Solution..."
        span="WHENEVER THE QUESTION IS YOUR TECH NEEDS!"
        text="With a belief that technology is not just a tool but a way of enhancing everyday life, we have created a platform to meet your needs. Whether you're looking for cutting-edge devices, expert advice, or unparalleled support, our team is here to provide a seamless experience tailored just for you."
        showIcons={false}
      />
    </motion.div>
  );
};

export default TechOverview;
