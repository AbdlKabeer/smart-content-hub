import { useState } from 'react';
import { Link } from 'react-router-dom';

// Card Component
export const Card: React.FC = () => {
  return (
    <Link
      to="/videos"
      className="flex flex-col items-center max-h-20 bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700 overflow-hidden"
    >
      <div className="w-full md:w-48 h-96 md:h-auto overflow-hidden">
        <img
          className="object-cover w-full h-full rounded-t-lg md:rounded-none md:rounded-s-lg"
          src="https://avatars.githubusercontent.com/u/95700260?s=400&u=8a038fc4fa00588887195b84026eb610c9213b4f&v=4"
          alt=""
        />
      </div>
      <div className="flex flex-col justify-between p-4 leading-normal overflow-hidden">
        <h5 className="text-sm font-semibold tracking-tight text-gray-900 dark:text-white line-clamp-1">
          Noteworthy technology acquisitions 2021
        </h5>
        <p className="text-sm font-normal text-gray-700 dark:text-gray-400 line-clamp-2">
          Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
        </p>
      </div>
    </Link>
  );
};

// Feedback Modal Component
interface Feedback {
  helpful: 'yes' | 'no' | null;
  moreContent: 'yes' | 'no' | null;
}

interface FeedbackModalProps {
  isVisible: boolean;
  onClose: () => void;
  onFeedbackSubmit: (feedback: Feedback) => void;
}

const FeedbackModal: React.FC<FeedbackModalProps> = ({
  isVisible,
  onClose,
  onFeedbackSubmit,
}) => {
  const [feedback, setFeedback] = useState<Feedback>({ helpful: null, moreContent: null });

  const handleSubmit = () => {
    onFeedbackSubmit(feedback);
    onClose();
  };

  return (
    isVisible && (
      <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div className="bg-white p-6 rounded-lg shadow-md w-96">
          <h3 className="text-xl font-semibold mb-4">Feedback</h3>

          <div className="mb-4">
            <p className="font-medium">Was this resource helpful?</p>
            <div className="flex gap-4 mt-2">
              <button
                className={`px-4 py-2 border rounded-md ${feedback.helpful === 'yes' ? 'bg-blue-500 text-white' : ''}`}
                onClick={() => setFeedback({ ...feedback, helpful: 'yes' })}
              >
                Yes
              </button>
              <button
                className={`px-4 py-2 border rounded-md ${feedback.helpful === 'no' ? 'bg-red-500 text-white' : ''}`}
                onClick={() => setFeedback({ ...feedback, helpful: 'no' })}
              >
                No
              </button>
            </div>
          </div>

          <div className="mb-4">
            <p className="font-medium">Would you like more content like this?</p>
            <div className="flex gap-4 mt-2">
              <button
                className={`px-4 py-2 border rounded-md ${feedback.moreContent === 'yes' ? 'bg-blue-500 text-white' : ''}`}
                onClick={() => setFeedback({ ...feedback, moreContent: 'yes' })}
              >
                Yes
              </button>
              <button
                className={`px-4 py-2 border rounded-md ${feedback.moreContent === 'no' ? 'bg-red-500 text-white' : ''}`}
                onClick={() => setFeedback({ ...feedback, moreContent: 'no' })}
              >
                No
              </button>
            </div>
          </div>

          <div className="flex justify-between">
            <button
              className="px-4 py-2 bg-gray-300 rounded-md"
              onClick={onClose}
            >
              Close
            </button>
            <button
              className="px-4 py-2 bg-blue-500 text-white rounded-md"
              onClick={handleSubmit}
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    )
  );
};

// Main Video Component
const Video: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);

  const triggerModal = () => {
    setModalVisible(true);
  };

  const handleFeedbackSubmit = (feedback: { helpful: string | null; moreContent: string | null }) => {
    console.log('Feedback submitted:', feedback);
    // Handle feedback submission (e.g., send to server)
  };

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="col-span-2">
          <h3 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            Your browser does not support the video tag.
          </h3>
          <video className="w-full" controls onEnded={triggerModal}>
            <source src="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>

          <p className="py-4">
            Learn how to install Tailwind CSS with Flowbite for your React project and start developing
            modern web applications using interactive elements based on utility classes.
          </p>
        </div>

        <div>
          <h3 className="mb-2 text-xl font-semibold tracking-tight text-gray-900 dark:text-white">Related</h3>
          <div className="flex flex-col gap-2">
            <Card />
            <Card />
            <Card />
            <Card />
            <Card />
            <Card />
          </div>
        </div>
      </div>

      {/* Feedback Modal */}
      <FeedbackModal
        isVisible={modalVisible}
        onClose={() => setModalVisible(false)}
        onFeedbackSubmit={handleFeedbackSubmit}
      />
    </>
  );
};

export default Video;
