// components/ui/Dialog.js
import Modal from "react-modal";

export function Dialog({ isOpen, onClose, children }) {
  return (
    <Modal isOpen={isOpen} onRequestClose={onClose} className="p-6 bg-white rounded shadow-lg w-1/2 mx-auto mt-10">
      <button onClick={onClose} className="absolute top-2 right-2 text-gray-600">✖</button>
      {children}
    </Modal>
  );
}
