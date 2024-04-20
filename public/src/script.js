let user_ip;
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await set_user_ip();
  } catch (error) {
    console.error("Error setting user IP:", error);
    user_ip = "1.2.3.4"; // Fallback IP in case of error
  }

  // Initialize chat only after user agreement by clicking 'Agree'
  const userInputField = document.getElementById("user-input");
  userInputField.addEventListener("focus", adjustInputPosition);
  userInputField.addEventListener("blur", resetInputPosition);

  // Detect Facebook in-app browser
  if (/FBAN|FBAV/i.test(navigator.userAgent)) {
    // Best current workaround to android webview keyboard overlap bug.
    displayModal();

    document
      .getElementById("agreeButton")
      .addEventListener("click", function () {
        closeModal();
        initializeChat();
      });
    document.body.classList.add("facebook-in-app");
  } else {
    initializeChat();
  }
});
/**
 * Display a chat consent modal.
 */
function displayModal() {
  document.getElementById("chatConsentModal").style.display = "block";
}

/**
 * Close the chat consent modal.
 */
function closeModal() {
  document.getElementById("chatConsentModal").style.display = "none";
}

/**
 *  This method adjusts the keyboard to fit into the viewport properly.
 */
function adjustInputPosition() {
  if (document.body.classList.contains("facebook-in-app")) {
    const chatContainer = document.getElementById("chat-container");
    const keyboardHeightApprox = 400;
    chatContainer.style.paddingBottom = `${keyboardHeightApprox}px`;
    window.setTimeout(() => {
      chatContainer.scrollIntoView({ behavior: "smooth", block: "end" });
    }, 0);
  }
}

/**
 * Reset the input values on blur. Unfortunately we cannot include when the back button is pressed.
 */
function resetInputPosition() {
  if (document.body.classList.contains("facebook-in-app")) {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.paddingBottom = "0px";
  }
}

/**
 * Fetches the user's IP address and sets it in the global user_ip variable.
 */
async function set_user_ip() {
  try {
    const response = await fetch("https://ipinfo.io/json");
    if (!response.ok) {
      throw new Error("Failed to fetch IP address");
    }
    const data = await response.json();
    user_ip = data.ip;
  } catch (error) {
    console.error("Failed to fetch IP address:", error);
    throw error;
  }
}
/**
 * Sets up event listeners for the chat interface.
 */
function initializeChat() {
  const threadId = sessionStorage.getItem("threadId");

  // If no existing thread is found, send a default message for assistance.
  if (!threadId) {
    const urlParams = new URLSearchParams(window.location.search);
    const prompt_message = urlParams.get("prompt_message");
    if (!prompt_message) {
      sendUserMessage("Hello Samm, I need help with my renovation project.");
    } else {
      sendUserMessage(prompt_message);
    }
  }

  // Event listener for the send message button.
  document.getElementById("send-button").addEventListener("click", () => {
    fbq("track", "Lead");
    const userInputField = document.getElementById("user-input");
    const userInput = userInputField.value.trim();

    // Proceed only if the user input is not empty.
    if (userInput) {
      sendUserMessage(userInput);
      clearUserInputField(userInputField);
      scrollToBottom("chat-history");
    }
  });
}

/**
 * Sends a message entered by the user and displays it in the chat history.
 * @param {string} message - The message to be sent.
 */
async function sendUserMessage(message) {
  displayMessage(message, "user", "images/user_dp.png");

  const threadId = sessionStorage.getItem("threadId");

  const requestBody = threadId
    ? { message, user_ip, threadId }
    : { message, user_ip };

  // Temporarily disables the send button to prevent multiple submissions.
  toggleSendButtonDisabledState(true);

  // Show a loading message while waiting for the response.
  loadingMessage("samm", "images/samm_dp.png");

  const botResponse = await postMessageToServer(requestBody);
  displayMessage(botResponse.assistant_response, "samm", "images/samm_dp.png");

  // Re-enable the send button after receiving the response.
  toggleSendButtonDisabledState(false);

  // Scroll to the bottom of the chat history after displaying the response.
  scrollToBottom("chat-history");

  // Update the threadId in sessionStorage if it's a new conversation.
  if (botResponse.thread_id && !threadId) {
    sessionStorage.setItem("threadId", botResponse.thread_id);
  }
}

/**
 * Posts the user's message to the server and waits for the response.
 * @param {Object} body - The request body, containing the message and optionally the threadId.
 * @returns {Promise<Object>} The response from the server.
 */
async function postMessageToServer(body) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return response.json();
}

/**
 * Displays a message in the chat history.
 * @param {string} message - The message content.
 * @param {string} sender - The sender type ('user' or 'bot').
 * @param {string} imageUrl - The URL of the sender's display picture.
 */
function displayMessage(message, sender, imageUrl) {
  const chatHistory = document.getElementById("chat-history");

  // Directly use the loaderMessageElement reference to remove the loader
  if (loaderMessageElement) {
    chatHistory.removeChild(loaderMessageElement);
    loaderMessageElement = null;
  }

  // Create and add the new message
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.innerHTML = `<img src="${imageUrl}" alt="${sender}"><div>${message}</div>`;
  chatHistory.appendChild(messageDiv);
}

let loaderMessageElement = null;

/**
 * Displays a loading message in the chat history.
 */
function loadingMessage(sender, imageUrl) {
  const chatHistory = document.getElementById("chat-history");

  // Remove existing loader message if present
  if (loaderMessageElement) {
    chatHistory.removeChild(loaderMessageElement);
    loaderMessageElement = null; // Reset the reference
  }

  // Create a new loader message
  loaderMessageElement = document.createElement("div");
  loaderMessageElement.classList.add("message", sender);
  loaderMessageElement.innerHTML = `<img src="${imageUrl}" alt="${sender}"><div class="loader-chat"></div>`;
  chatHistory.appendChild(loaderMessageElement);
}

/**
 * Clears the user input field.
 * @param {HTMLElement} userInputField - The user input field element.
 */
function clearUserInputField(userInputField) {
  userInputField.value = "";
}

/**
 * Scrolls the chat history to the bottom.
 * @param {string} elementId - The ID of the chat history container.
 */
function scrollToBottom(elementId) {
  const element = document.getElementById(elementId);
  element.scrollTop = element.scrollHeight;
}

/**
 * Toggles the disabled state of the send button.
 * @param {boolean} state - The desired disabled state.
 */
function toggleSendButtonDisabledState(state) {
  document.getElementById("send-button").disabled = state;
}
