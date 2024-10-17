"use client";
import React from 'react'
import { LayoutProps } from '@/app/layout'
import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from 'next/navigation';

const variants = {
  hidden: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};


export default function Transition( {children}: LayoutProps ) {
  const pathname = usePathname();


  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial="hidden"
        animate="enter"
        exit="exit"
        variants={variants}
        transition={{ duration: 0.25, ease: "easeInOut" }}
      >
        {children}
     </motion.div>
    </AnimatePresence>
  )
}
