import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaGithub } from 'react-icons/fa';
import { MdEmail, MdSend, MdCheckCircle, MdInfo } from 'react-icons/md';


export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.id]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-[#FEFEF4] pt-24 pb-16 text-[#222426]">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <span className="text-xs font-semibold text-[#E5BD1A] uppercase tracking-widest mb-3 block">Get in Touch</span>
          <h1 className="font-display font-bold text-3xl sm:text-5xl text-[#222426] mb-4">Contact Us</h1>
          <p className="text-[#4F504E] max-w-xl mx-auto">
            Have questions about SafeRoad AI, or want to contribute to the code? Send us a message or find us on GitHub.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          {/* Left Column: Contact Info */}
          <div className="md:col-span-4 space-y-6">
            <div className="rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] p-6 shadow-sm space-y-5">
              <div>
                <h3 className="font-display font-bold text-xl text-[#222426]">SafeRoad AI</h3>
                <p className="text-xs text-[#E5BD1A] font-semibold mt-0.5">Predict Risks. Prevent Accidents.</p>
              </div>

              <div className="space-y-4 pt-2 border-t border-[#222426]/5">
                {/* Email */}
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-lg bg-[#FEFEF4] border border-[#222426]/10 flex items-center justify-center shrink-0 mt-0.5">
                    <MdEmail className="text-[#E5BD1A] text-lg" />
                  </div>
                  <div>
                    <p className="text-xs text-[#7E7F81] font-semibold">Email</p>
                    <a href="mailto:uupparaveeranji@gmail.com" className="text-sm font-semibold text-[#222426] hover:underline">
                      uupparaveeranji@gmail.com
                    </a>
                  </div>
                </div>
              </div>

              {/* GitHub Button — solid black */}
              <div className="pt-4 border-t border-[#222426]/5">
                <a
                  href="https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 text-xs font-semibold px-4 py-2.5 rounded-xl text-[#FEFEF4] bg-[#222426] hover:opacity-80 transition-all duration-300 shadow-sm"
                >
                  <FaGithub /> GitHub Repository
                </a>
              </div>
            </div>

            {/* Info block */}
            <div className="p-4 bg-[#FAF9F2] border border-[#222426]/10 rounded-2xl flex items-start gap-2.5 shadow-sm">
              <MdInfo className="text-[#E5BD1A] text-lg shrink-0 mt-0.5" />
              <p className="text-xs text-[#4F504E] leading-relaxed">
                This project is open-source. For feature suggestions or reporting bugs in model predictions, please open an issue on our GitHub repository.
              </p>
            </div>
          </div>

          {/* Right Column: Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="md:col-span-8 rounded-2xl border border-[#222426]/10 bg-[#FAF9F2] shadow-sm overflow-hidden"
          >
            <div className="px-6 py-5 border-b border-[#222426]/5">
              <h2 className="font-display font-semibold text-lg text-[#222426]">Send a Message</h2>
              <p className="text-xs text-[#7E7F81] mt-0.5">We'll get back to you as soon as possible.</p>
            </div>
            <div className="p-6">
              <AnimatePresence mode="wait">
                {!submitted ? (
                  <motion.form
                    key="form"
                    initial={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onSubmit={handleSubmit}
                    className="space-y-4"
                  >
                    {/* Name & Email */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="name" className="block text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2">Name</label>
                        <input
                          id="name"
                          type="text"
                          value={form.name}
                          onChange={handleChange}
                          required
                          placeholder="Your Name"
                          className="w-full px-4 py-3 rounded-xl text-[#222426] text-sm bg-[#FEFEF4] border border-[#222426]/10 focus:outline-none focus:border-[#FAD02C]/60 transition-colors duration-200 placeholder-[#7E7F81]/50"
                        />
                      </div>
                      <div>
                        <label htmlFor="email" className="block text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2">Email</label>
                        <input
                          id="email"
                          type="email"
                          value={form.email}
                          onChange={handleChange}
                          required
                          placeholder="Your Email"
                          className="w-full px-4 py-3 rounded-xl text-[#222426] text-sm bg-[#FEFEF4] border border-[#222426]/10 focus:outline-none focus:border-[#FAD02C]/60 transition-colors duration-200 placeholder-[#7E7F81]/50"
                        />
                      </div>
                    </div>

                    {/* Subject */}
                    <div>
                      <label htmlFor="subject" className="block text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2">Subject</label>
                      <input
                        id="subject"
                        type="text"
                        value={form.subject}
                        onChange={handleChange}
                        required
                        placeholder="Subject of message"
                        className="w-full px-4 py-3 rounded-xl text-[#222426] text-sm bg-[#FEFEF4] border border-[#222426]/10 focus:outline-none focus:border-[#FAD02C]/60 transition-colors duration-200 placeholder-[#7E7F81]/50"
                      />
                    </div>

                    {/* Message */}
                    <div>
                      <label htmlFor="message" className="block text-xs font-semibold text-[#7E7F81] uppercase tracking-wider mb-2">Message</label>
                      <textarea
                        id="message"
                        value={form.message}
                        onChange={handleChange}
                        rows={5}
                        required
                        placeholder="Your message here..."
                        className="w-full px-4 py-3 rounded-xl text-[#222426] text-sm bg-[#FEFEF4] border border-[#222426]/10 focus:outline-none focus:border-[#FAD02C]/60 transition-colors duration-200 resize-none placeholder-[#7E7F81]/50"
                      />
                    </div>

                    {/* Submit */}
                    <motion.button
                      type="submit"
                      disabled={loading}
                      whileHover={{ scale: loading ? 1 : 1.01 }}
                      whileTap={{ scale: loading ? 1 : 0.99 }}
                      className="btn-primary w-full py-3.5 justify-center rounded-xl font-semibold"
                      id="contact-submit"
                    >
                      {loading ? (
                        <>
                          <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                            className="w-4 h-4 rounded-full border-2 border-[#222426] border-t-transparent"
                          />
                          Sending...
                        </>
                      ) : (
                        <>
                          <MdSend />
                          Send Message
                        </>
                      )}
                    </motion.button>
                  </motion.form>
                ) : (
                  <motion.div
                    key="success"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-12"
                  >
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: 'spring', bounce: 0.5, delay: 0.1 }}
                    >
                      <MdCheckCircle className="text-6xl text-[#00A843] mx-auto mb-4" />
                    </motion.div>
                    <h3 className="font-display font-bold text-[#222426] text-2xl mb-2">Message Sent!</h3>
                    <p className="text-[#4F504E] text-sm max-w-md mx-auto">
                      Thank you for contacting us. We've received your message and will reply as soon as possible.
                    </p>
                    <button
                      onClick={() => { setSubmitted(false); setForm({ name: '', email: '', subject: '', message: '' }); }}
                      className="mt-6 btn-secondary text-sm px-6 py-2.5 rounded-xl border border-[#222426]/10"
                      id="send-another"
                    >
                      Send Another Message
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>

      </div>
    </div>
  );
}
