/**
 * Accordion Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * FAQ accordion component displaying frequently asked questions in an
 * expandable/collapsible format.
 *
 * Features:
 *   - Expandable/collapsible question-answer pairs
 *   - Single active item at a time (toggle behavior)
 *   - Plus/minus icon indicators
 *   - Image illustration alongside questions
 *   - Smooth expand/collapse animations
 *   - Questions loaded from external data file
 *
 * Behavior:
 *   - Click question to expand answer
 *   - Click again to collapse
 *   - Opening new question closes previously opened one
 *   - Icons toggle between plus (collapsed) and minus (expanded)
 *
 * State Management:
 *   - activeIndex: Index of currently open accordion item (null if all closed)
 *
 * Data Source:
 *   - AccordionData.js - Array of {question, answer} objects
 *
 * Icons:
 *   - AiOutlinePlus - Collapsed state indicator
 *   - AiOutlineMinus - Expanded state indicator
 *
 * @component
 * @returns {React.ReactElement} FAQ accordion with expandable items
 */
import "./Accordion.scss";
import accordionData from "./AccordionData";
import { useState } from "react";
import { AiOutlinePlus, AiOutlineMinus } from "react-icons/ai";
import faq from "../../assets/faq1.webp";

const Accordion = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  const toggleAccordion = (index) => {
    setActiveIndex((prevIndex) => (prevIndex === index ? null : index));
  };

  return (
    <div className="accordion">
      <h2 className="accordion__title">Frequently Asked Questions</h2>

      <div className="accordion__wrapper">
        <img
          src={faq}
          alt="A modern electronics store with gadgets on display."
          className="accordion__img"
        />

        <div className="accordion__questions">
          {accordionData.map((q, index) => (
            <div key={index} className="accordion__item">
              <div
                className="accordion__box"
                onClick={() => toggleAccordion(index)}>
                <h3 className="accordion__question">{q.question}</h3>
                {activeIndex === index ? <AiOutlineMinus /> : <AiOutlinePlus />}
              </div>
              {activeIndex === index && (
                <div className="accordion__answer">{q.answer}</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Accordion;
