import { motion } from "framer-motion";
import PropTypes from "prop-types";

const AnimatedPage = ({
  children,
  animationVariants = null,
  transition = null,
}) => {
  const defaultAnimation = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 20 },
  };

  return (
    <motion.div
      variants={animationVariants || defaultAnimation}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={transition || { duration: 0.3 }}>
      {children}
    </motion.div>
  );
};

AnimatedPage.propTypes = {
  children: PropTypes.node.isRequired,
  animationVariants: PropTypes.object,
  transition: PropTypes.object,
};

export default AnimatedPage;
