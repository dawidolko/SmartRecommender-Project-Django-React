import React from "react";
import { motion } from "framer-motion";

const StatCard = ({ name, icon: Icon, value, color, variant }) => {
  const cardModifier = variant || "first";

  return (
    <motion.div
      whileHover={{ y: -5, boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)" }}>
      <div
        className={`stat_Cards__content stat_Cards__content-${cardModifier}`}>
        <span className="stat_Cards__icon">
          {Icon && <Icon size={30} className="mr-2" style={{ color }} />}
          {name}
        </span>
        <p className="stat_Cards__text">{value}</p>
      </div>
    </motion.div>
  );
};

export default StatCard;
