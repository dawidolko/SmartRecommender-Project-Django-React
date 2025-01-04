const AnimationVariants = {
  modalAnimation: {
    initial: {
      opacity: 0,
      y: 100,
    },
    animate: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.4,
        ease: "easeOut",
      },
    },
    exit: {
      opacity: 0,
      y: 50,
      transition: {
        duration: 0.3,
        ease: "easeIn",
      },
    },
  },

  overlayAnimation: {
    initial: {
      opacity: 0,
    },
    animate: {
      opacity: 1,
      transition: {
        duration: 0.25,
        ease: "linear",
      },
    },
    exit: {
      opacity: 0,
      transition: {
        duration: 0.2,
        ease: "linear",
      },
    },
  },

  fadeIn: {
    initial: {
      y: -100,
      opacity: 0,
    },
    animate: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: "easeOut",
      },
    },
  },

  fadeIn2: {
    initial: {
      opacity: 0,
      scale: 0.7,
    },
    animate: {
      scale: 1,
      opacity: 1,
      transition: {
        duration: 0.7,
        ease: "easeOut",
      },
    },
  },

  slideIn: {
    initial: {
      x: 150,
      opacity: 0,
    },
    animate: {
      x: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
        ease: "easeOut",
      },
    },
    exit: {
      x: -150,
      opacity: 0,
      transition: {
        duration: 0.4,
        ease: "easeIn",
      },
    },
  },
};

export default AnimationVariants;
