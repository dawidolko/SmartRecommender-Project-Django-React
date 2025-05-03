import "./Team.scss";
import teamData from "./TeamData";
import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import AnimationVariants from "../AnimationVariants/AnimationVariants";
import { FaFacebookF, FaTwitter, FaInstagram } from "react-icons/fa";

const Team = () => {
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  return (
    <motion.section
      className="team"
      variants={AnimationVariants.slideIn}
      initial="initial"
      animate={isInView ? "animate" : "initial"}
      ref={ref}>
      <h2 className="team__title">Meet Our Project Team</h2>
      <p className="team__subtitle">
        Get to know the talented individuals behind SmartRecommender. Our team
        combines technical expertise and academic guidance to create this
        innovative product recommendation system.
      </p>
      <motion.div
        variants={AnimationVariants.slideIn}
        initial="initial"
        animate={isInView ? "animate" : "initial"}
        ref={ref}
        className="team__body container">
        {teamData.map((item) => (
          <div className="team__card" key={item.id}>
            <img
              className="team__img"
              src={item.img}
              alt={`Technology Expert: ${item.name}`}
            />
            <div className="team__text">
              <h3 className="team__name">{item.name}</h3>
              <p className="team__role">{item.role}</p>
              <div className="team__icons">
                {item.facebook && (
                  <a href={item.facebook} target="_blank" rel="noreferrer">
                    <FaFacebookF className="team__icon" />
                  </a>
                )}
                {item.twitter && (
                  <a href={item.twitter} target="_blank" rel="noreferrer">
                    <FaTwitter className="team__icon" />
                  </a>
                )}
                {item.instagram && (
                  <a href={item.instagram} target="_blank" rel="noreferrer">
                    <FaInstagram className="team__icon" />
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </motion.div>
    </motion.section>
  );
};

export default Team;
