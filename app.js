// Networking Fundamentals - 8-Week Study Plan Curriculum Data
const curriculum = [
  {
    week: 1,
    title: "Week 1: Introduction & Network Devices",
    topic: "Introduction & Network Devices",
    videos: [
      { title: "Lesson 1a: Network Devices - Hosts, IP, Networks", id: "bj-Yfakjllc" },
      { title: "Lesson 1b: Hub, Bridge, Switch, Router", id: "H7-NR3Q3BeI" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Map Your Local Topology</strong></p>
        <p>Draw a sketch of your home network. Label the hosts (smartphones, PCs), the switch (usually built into your home router), and the gateway router connecting you to the ISP.</p>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Inspect Host Network Settings</strong></p>
        <p>Open a terminal on your device and run the following command to find your IP and MAC address:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('ip addr')">Copy</button>
          </div>
          <code>ip addr</code>
        </div>
        <p>Locate the interface name (e.g., <code>eth0</code> or <code>wlan0</code>), your IPv4 address (after <code>inet</code>), and physical hardware address (after <code>link/ether</code>).</p>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 3: Analyze Device Differences</strong></p>
        <p>Write a brief summary of how a Hub (repeater), a Bridge/Switch (MAC forwarding), and a Router (IP forwarding) process frames/packets differently.</p>
      </div>
    `,
    quiz: [
      {
        question: "At which layer of the OSI model does a Switch primarily operate?",
        options: [
          "Layer 1: Physical Layer",
          "Layer 2: Data Link Layer",
          "Layer 3: Network Layer",
          "Layer 4: Transport Layer"
        ],
        correct: 1,
        explanation: "Switches forward frames based on MAC addresses, which reside at the Data Link Layer (Layer 2)."
      },
      {
        question: "What is the key functional difference between a Hub and a Switch?",
        options: [
          "A Switch floods all traffic out all ports, while a Hub learns MAC addresses.",
          "A Hub operates at Layer 3, while a Switch operates at Layer 2.",
          "A Switch learns MAC addresses to send frames selectively; a Hub repeats all signals to all ports.",
          "A Hub performs routing tables lookups, a Switch does not."
        ],
        correct: 2,
        explanation: "Hubs are simple physical-layer repeaters that echo traffic everywhere, whereas Switches learn MAC addresses and forward frames selectively to reduce collision domains."
      },
      {
        question: "Which device is responsible for moving packets between different logical networks (subnets)?",
        options: [
          "Network Bridge",
          "Layer-2 Switch",
          "Repeater",
          "Router"
        ],
        correct: 3,
        explanation: "Routers operate at the Network Layer (Layer 3) and forward packets based on logical IP addresses between distinct subnets."
      }
    ]
  },
  {
    week: 2,
    title: "Week 2: The OSI Model Deep Dive",
    topic: "OSI Model Deep Dive",
    videos: [
      { title: "Lesson 2a: OSI Model: Practical Perspective", id: "LkolbURrtTs" },
      { title: "Lesson 2b: OSI Model: Practical Perspective - Part 2", id: "0aGqGKrRE0g" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: List the 7 Layers</strong></p>
        <p>Write out the 7 layers of the OSI model from Layer 7 (Application) down to Layer 1 (Physical). Create a mnemonic to help memorize them (e.g., "Please Do Not Throw Sausage Pizza Away").</p>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Map Protocols and Data Units (PDUs)</strong></p>
        <p>For each layer, list the corresponding PDU name (e.g., Segment for Layer 4, Packet for Layer 3, Frame for Layer 2, Bits for Layer 1) and note at least two common protocols for each.</p>
      </div>
    `,
    quiz: [
      {
        question: "Which layer of the OSI model is responsible for end-to-end communication, session multiplexing via port numbers, and reliability?",
        options: [
          "Layer 2: Data Link Layer",
          "Layer 3: Network Layer",
          "Layer 4: Transport Layer",
          "Layer 7: Application Layer"
        ],
        correct: 2,
        explanation: "The Transport Layer (Layer 4) manages ports (like TCP/UDP) and handles end-to-end segments, flow control, and error recovery."
      },
      {
        question: "What is the term for wrapping data in headers and trailers as it moves down the OSI stack?",
        options: [
          "Decapsulation",
          "Multiplexing",
          "Encapsulation",
          "Summarization"
        ],
        correct: 2,
        explanation: "Encapsulation is the process of enclosing upper-layer data inside a lower-layer protocol header/trailer."
      }
    ]
  },
  {
    week: 3,
    title: "Week 3: How Hosts Communicate & ARP",
    topic: "How Hosts Communicate & ARP",
    videos: [
      { title: "Lesson 3: Hosts speaking on Internet - Part 1", id: "gYN2qN11-wE" },
      { title: "Lesson 3: Hosts speaking on Internet - Part 2", id: "JI9Zm2tbUoE" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Check Default Gateway</strong></p>
        <p>Identify where your computer sends all non-local subnet traffic. Run the route lookup command in terminal:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('ip route show')">Copy</button>
          </div>
          <code>ip route show</code>
        </div>
        <p>The IP address listed next to <code>default via</code> is your Default Gateway.</p>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Inspect ARP Cache Table</strong></p>
        <p>Check the mapping of IP addresses to physical MAC addresses stored on your host:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('arp -an')">Copy</button>
          </div>
          <code>arp -an</code>
        </div>
      </div>
    `,
    quiz: [
      {
        question: "When a host wants to transmit data to another host, how does it determine whether the destination is local or remote?",
        options: [
          "It queries the DNS server.",
          "It performs a bitwise AND comparison using its IP, subnet mask, and the destination IP.",
          "It broadcasts an ARP request.",
          "It automatically forwards all packets to the default gateway."
        ],
        correct: 1,
        explanation: "Hosts compare their own subnet prefix (calculated by ANDing their IP and subnet mask) with the destination IP's subnet prefix to decide if the destination is on the local link."
      },
      {
        question: "What is the purpose of ARP (Address Resolution Protocol)?",
        options: [
          "To translate hostnames like google.com to IP addresses.",
          "To discover the MAC address of a host given its IP address.",
          "To dynamically assign IP configurations to clients.",
          "To secure TCP connections with cryptographic certificates."
        ],
        correct: 1,
        explanation: "ARP maps logical IP addresses (Layer 3) to hardware MAC addresses (Layer 2) on a local network segment."
      }
    ]
  },
  {
    week: 4,
    title: "Week 4: Switch Operations & MAC Tables",
    topic: "Switch Operations & MAC Tables",
    videos: [
      { title: "Lesson 4: Switch Operations - Part 1", id: "AhOU2eOpmX0" },
      { title: "Lesson 4: Switch Operations - Part 2", id: "G7GyWjJtjNs" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Detail Switch Functions</strong></p>
        <p>Write an explanation of how a Switch behaves when it receives a frame. Detail the 3 main actions:</p>
        <ul>
          <li><strong>Learning:</strong> Checking the source MAC address and updating the CAM table.</li>
          <li><strong>Forwarding/Filtering:</strong> Checking the destination MAC and selectively sending it.</li>
          <li><strong>Flooding:</strong> Broadcasting the frame when the destination MAC is unknown or is a broadcast (FF:FF:FF:FF:FF:FF).</li>
        </ul>
      </div>
    `,
    quiz: [
      {
        question: "What does a switch do when it receives a unicast frame with a destination MAC address that is NOT in its CAM table?",
        options: [
          "It drops the frame.",
          "It floods the frame out all ports except the port it arrived on.",
          "It sends an ARP request to find it.",
          "It forwards it to the default gateway."
        ],
        correct: 1,
        explanation: "If a switch does not know which port matches a destination unicast MAC, it floods the frame out all other ports (Unknown Unicast Flooding)."
      },
      {
        question: "How does a switch learn MAC address table entries?",
        options: [
          "By examining the source MAC address of incoming frames.",
          "By examining the destination MAC address of incoming frames.",
          "By querying a central Domain Controller.",
          "By periodic network scans."
        ],
        correct: 0,
        explanation: "A switch dynamically populates its CAM table by looking at the SOURCE MAC address of incoming frames on each interface."
      }
    ]
  },
  {
    week: 5,
    title: "Week 5: Router Operations & Forwarding",
    topic: "Router Operations & Forwarding",
    videos: [
      { title: "Lesson 5: Router Operations - Part 1", id: "AzXys5kxpAM" },
      { title: "Lesson 5: Router Forwarding - Part 2", id: "Ep-x_6kggKA" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Inspect System Routing Table</strong></p>
        <p>Look at your local system's active IP routing table rules using:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('route -n')">Copy</button>
          </div>
          <code>route -n</code>
        </div>
        <p>Note how specific routes are evaluated alongside general gateway routes.</p>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Header Changes Across Hops</strong></p>
        <p>Sketch a packet traversing two routers. Illustrate how the Source/Destination MAC addresses are rewritten at each hop, whereas the Source/Destination IP addresses remain untouched.</p>
      </div>
    `,
    quiz: [
      {
        question: "When a router forwards an IP packet from one ethernet network segment to another, what occurs?",
        options: [
          "The source and destination IP addresses are swapped.",
          "The router strips the Layer 2 header and builds a new Layer 2 header with new MAC addresses.",
          "The router modifies the TCP sequence numbers.",
          "The entire packet payload is encrypted."
        ],
        correct: 1,
        explanation: "Routers strip the incoming Layer 2 frame to read the Layer 3 IP header. To forward it, they repackage the packet in a new Layer 2 frame containing the new hop's MAC addresses."
      },
      {
        question: "If a router's routing table has multiple matching entries for a destination IP address, how does it choose which route to use?",
        options: [
          "It uses the first entry matching the IP.",
          "It uses the entry with the longest prefix match (most specific subnet mask).",
          "It rounds-robin balances across all matches.",
          "It defaults to forwarding to the DNS server."
        ],
        correct: 1,
        explanation: "The router selects the path with the Longest Prefix Match (the most specific network mask) for the destination IP."
      }
    ]
  },
  {
    week: 6,
    title: "Week 6: Subnetting & Route Summarization",
    topic: "Subnetting & Route Summarization",
    videos: [
      { title: "Lesson 5: Route Summarization - Part 3", id: "zmxLg4jV0ts" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Practice Summarization</strong></p>
        <p>Summarize the following block of networks into a single route prefix:</p>
        <ul>
          <li><code>192.168.0.0/24</code></li>
          <li><code>192.168.1.0/24</code></li>
          <li><code>192.168.2.0/24</code></li>
          <li><code>192.168.3.0/24</code></li>
        </ul>
        <p><em>Hint: Write them in binary and find the matching common bits. (Ans: 192.168.0.0/22)</em></p>
      </div>
    `,
    quiz: [
      {
        question: "What is the single summarized route for 172.16.8.0/24 and 172.16.9.0/24?",
        options: [
          "172.16.8.0/23",
          "172.16.0.0/16",
          "172.16.8.0/22",
          "172.16.10.0/23"
        ],
        correct: 0,
        explanation: "172.16.8.0 (binary ...00001000) and 172.16.9.0 (binary ...00001001) share their first 23 bits in common. Summarizing them merges the subnets into 172.16.8.0/23."
      },
      {
        question: "How many host IP addresses are usable in a subnet with a /30 prefix?",
        options: [
          "4",
          "2",
          "6",
          "1"
        ],
        correct: 1,
        explanation: "A /30 network has 4 addresses total. Subtracting the Network ID and Broadcast IP leaves 2 usable host IP addresses (often used for point-to-point router links)."
      }
    ]
  },
  {
    week: 7,
    title: "Week 7: Network Protocols in Action",
    topic: "Network Protocols in Action",
    videos: [
      { title: "Lesson 6: Core Network Protocols Overview", id: "E5bSumTAHZE" },
      { title: "Telnet Hands-on: HTTP vs HTML", id: "ArXMa111x7A" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Test DNS Lookups</strong></p>
        <p>Query nameservers to resolve domain IP info:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('nslookup google.com')">Copy</button>
          </div>
          <code>nslookup google.com</code>
        </div>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Raw HTTP Retrieval</strong></p>
        <p>Retrieve headers from a web server directly using curl:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('curl -I http://example.com')">Copy</button>
          </div>
          <code>curl -I http://example.com</code>
        </div>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 3: DHCP DORA</strong></p>
        <p>Review the 4 DHCP protocol packet exchange steps: <strong>D</strong>iscover (broadcast client request), <strong>O</strong>ffer (router proposal), <strong>R</strong>equest (client acceptance), and <strong>A</strong>cknowledge (server confirmation).</p>
      </div>
    `,
    quiz: [
      {
        question: "Which protocol is responsible for translating human-friendly names (e.g. google.com) to machine IP addresses?",
        options: [
          "DHCP",
          "DNS",
          "ARP",
          "HTTP"
        ],
        correct: 1,
        explanation: "DNS (Domain Name System) acts as the phonebook of the internet, resolving domain names into numerical IP addresses."
      },
      {
        question: "What is the correct order of messages in a standard DHCP transaction?",
        options: [
          "Request, Offer, Discover, Acknowledge",
          "Discover, Request, Offer, Acknowledge",
          "Discover, Offer, Request, Acknowledge",
          "Offer, Discover, Request, Acknowledge"
        ],
        correct: 2,
        explanation: "DHCP uses the DORA sequence: Discover, Offer, Request, Acknowledge."
      }
    ]
  },
  {
    week: 8,
    title: "Week 8: How Data Moves & Layer 5-7",
    topic: "How Data Moves & Layer 5-7",
    videos: [
      { title: "Lesson 7: Packet Traveling Walkthrough", id: "YJGGYKAV4pA" },
      { title: "Lesson 8: OSI Layers 5, 6, and 7", id: "2iFFRqzX3yE" }
    ],
    handsOn: `
      <div class="hands-on-step">
        <p><strong>Step 1: Perform path traceroute</strong></p>
        <p>Trace the intermediate router hops to an internet site:</p>
        <div class="terminal-block">
          <div class="terminal-header">
            <span><span class="terminal-dot dot-red"></span> <span class="terminal-dot dot-yellow"></span> <span class="terminal-dot dot-green"></span> bash</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('traceroute 8.8.8.8')">Copy</button>
          </div>
          <code>traceroute 8.8.8.8</code>
        </div>
      </div>
      <div class="hands-on-step">
        <p><strong>Step 2: Synthesize Packet Traveling</strong></p>
        <p>Combine everything you have learned: write a 2-paragraph summary explaining the step-by-step path a packet takes from clicking a link in a browser, query resolving, TCP handshake routing, MAC changes, and web rendering.</p>
      </div>
    `,
    quiz: [
      {
        question: "What does the traceroute command analyze to show the hop path to a target?",
        options: [
          "It tracks changes in MAC addresses.",
          "It sends packets with incrementing TTL (Time-to-Live) values in the IP header.",
          "It uses DNS recursion details.",
          "It establishes telnet sessions with intermediate routers."
        ],
        correct: 1,
        explanation: "Traceroute sends packets with increasing TTL values starting at 1. Each router decrements the TTL; when it hits 0, the router returns an ICMP Time Exceeded message, revealing its address."
      },
      {
        question: "Which layer of the OSI model handles data encryption, compression, and formatting conversions?",
        options: [
          "Layer 5: Session Layer",
          "Layer 6: Presentation Layer",
          "Layer 7: Application Layer",
          "Layer 4: Transport Layer"
        ],
        correct: 1,
        explanation: "The Presentation Layer (Layer 6) is responsible for syntax representation, translation, encryption, and data compression."
      }
    ]
  }
];

// App State
let currentWeekIdx = 0;
let activeVideoIdx = 0;
let currentQuizIdx = 0;
let timerSeconds = 3600; // 60 minutes
let timerInterval = null;

// DOM Elements
const sidebarNav = document.getElementById("sidebar-nav");
const currentWeekTitle = document.getElementById("current-week-title");
const videoTabsContainer = document.getElementById("video-tabs");
const videoIframe = document.getElementById("video-iframe");
const handsOnContainer = document.getElementById("hands-on-container");
const notesInput = document.getElementById("notes-input");
const saveStatus = document.getElementById("save-status");
const downloadNotesBtn = document.getElementById("download-notes-btn");

const quizQuestion = document.getElementById("quiz-question");
const quizOptions = document.getElementById("quiz-options");
const quizFeedback = document.getElementById("quiz-feedback");
const quizProgressText = document.getElementById("quiz-progress-text");
const quizNextBtn = document.getElementById("quiz-next-btn");

const timerDisplay = document.getElementById("timer-display");
const timerToggleBtn = document.getElementById("timer-toggle-btn");
const timerResetBtn = document.getElementById("timer-reset-btn");

const overallProgressText = document.getElementById("overall-progress-text");
const overallProgressBar = document.getElementById("overall-progress-bar");

// Initialize application
function initApp() {
  loadProgress();
  renderSidebar();
  loadWeek(currentWeekIdx);
  initTimer();
  updateOverallProgress();
  
  // Attach Notes Auto-Save
  notesInput.addEventListener("input", () => {
    saveNotes();
  });
  
  downloadNotesBtn.addEventListener("click", downloadNotes);
  
  // Attach Timer Controls
  timerToggleBtn.addEventListener("click", toggleTimer);
  timerResetBtn.addEventListener("click", resetTimer);
  
  // Quiz Next Button
  quizNextBtn.addEventListener("click", handleQuizNext);
}

// Render Sidebar Navigation
function renderSidebar() {
  sidebarNav.innerHTML = "";
  curriculum.forEach((weekData, idx) => {
    const isCompleted = getWeekCompletedState(idx);
    
    const navItem = document.createElement("div");
    navItem.className = `nav-item ${idx === currentWeekIdx ? 'active' : ''} ${isCompleted ? 'completed' : ''}`;
    navItem.innerHTML = `
      <div class="nav-checkbox" onclick="toggleWeekComplete(${idx}, event)"></div>
      <div class="nav-details" onclick="selectWeek(${idx})">
        <span class="nav-title">${weekData.title.split(":")[0]}</span>
        <span class="nav-subtitle">${weekData.topic}</span>
      </div>
    `;
    sidebarNav.appendChild(navItem);
  });
}

// Select Week
function selectWeek(idx) {
  currentWeekIdx = idx;
  activeVideoIdx = 0;
  currentQuizIdx = 0;
  
  // Update sidebar active class
  document.querySelectorAll(".nav-item").forEach((item, index) => {
    if (index === idx) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
  
  loadWeek(idx);
}

// Load curriculum information into UI
function loadWeek(weekIdx) {
  const weekData = curriculum[weekIdx];
  currentWeekTitle.textContent = weekData.title;
  
  // Video setup
  renderVideoTabs(weekData.videos);
  setVideo(weekData.videos[activeVideoIdx].id);
  
  // Hands-on Lab setup
  handsOnContainer.innerHTML = weekData.handsOn;
  
  // Load notes
  const savedNotes = localStorage.getItem(`notes-week-${weekIdx}`) || "";
  notesInput.value = savedNotes;
  
  // Load Quiz
  loadQuizQuestion();
}

// Render Video selection tabs
function renderVideoTabs(videos) {
  videoTabsContainer.innerHTML = "";
  if (videos.length <= 1) {
    videoTabsContainer.style.display = "none";
    return;
  }
  
  videoTabsContainer.style.display = "flex";
  videos.forEach((vid, idx) => {
    const btn = document.createElement("button");
    btn.className = `video-tab-btn ${idx === activeVideoIdx ? 'active' : ''}`;
    btn.textContent = `Part ${idx + 1}`;
    btn.title = vid.title;
    btn.addEventListener("click", () => {
      activeVideoIdx = idx;
      document.querySelectorAll(".video-tab-btn").forEach((b, i) => {
        b.classList.toggle("active", i === idx);
      });
      setVideo(vid.id);
    });
    videoTabsContainer.appendChild(btn);
  });
}

// Set iframe video source
function setVideo(id) {
  videoIframe.src = `https://www.youtube.com/embed/${id}?rel=0`;
}

// Save notes to localStorage
let saveTimeout = null;
function saveNotes() {
  saveStatus.textContent = "Typing...";
  saveStatus.classList.add("visible");
  
  if (saveTimeout) clearTimeout(saveTimeout);
  
  saveTimeout = setTimeout(() => {
    localStorage.setItem(`notes-week-${currentWeekIdx}`, notesInput.value);
    saveStatus.textContent = "Saved locally";
    setTimeout(() => {
      saveStatus.classList.remove("visible");
    }, 1000);
  }, 500);
}

// Download Notes as a .txt file
function downloadNotes() {
  const noteContent = notesInput.value;
  const blob = new Blob([noteContent], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `NetAcademy_Notes_Week_${currentWeekIdx + 1}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Quiz implementation
function loadQuizQuestion() {
  const weekData = curriculum[currentWeekIdx];
  const qData = weekData.quiz[currentQuizIdx];
  
  // Hide feedback
  quizFeedback.style.display = "none";
  quizNextBtn.disabled = true;
  
  quizProgressText.textContent = `Question ${currentQuizIdx + 1} of ${weekData.quiz.length}`;
  quizQuestion.textContent = qData.question;
  
  quizOptions.innerHTML = "";
  qData.options.forEach((opt, idx) => {
    const btn = document.createElement("button");
    btn.className = "quiz-option";
    btn.textContent = opt;
    btn.addEventListener("click", () => handleSelectOption(idx));
    quizOptions.appendChild(btn);
  });
}

function handleSelectOption(selectedIdx) {
  const qData = curriculum[currentWeekIdx].quiz[currentQuizIdx];
  const options = quizOptions.querySelectorAll(".quiz-option");
  
  // Disable options and highlight choice
  options.forEach((opt, idx) => {
    opt.classList.add("disabled");
    if (idx === qData.correct) {
      opt.classList.add("correct");
    } else if (idx === selectedIdx) {
      opt.classList.add("incorrect");
    }
  });
  
  // Render feedback explanation
  if (selectedIdx === qData.correct) {
    quizFeedback.className = "quiz-feedback success";
    quizFeedback.innerHTML = `<strong>Correct!</strong> ${qData.explanation}`;
  } else {
    quizFeedback.className = "quiz-feedback failure";
    quizFeedback.innerHTML = `<strong>Incorrect.</strong> ${qData.explanation}`;
  }
  quizFeedback.style.display = "block";
  quizNextBtn.disabled = false;
}

function handleQuizNext() {
  const weekData = curriculum[currentWeekIdx];
  if (currentQuizIdx < weekData.quiz.length - 1) {
    currentQuizIdx++;
    loadQuizQuestion();
  } else {
    // Completed the quiz for this week!
    alert("Congratulations! You have completed this week's quiz!");
    markWeekComplete(currentWeekIdx);
  }
}

// Timer Widget
function initTimer() {
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const minutes = Math.floor(timerSeconds / 60);
  const seconds = timerSeconds % 60;
  timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function toggleTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
    timerToggleBtn.textContent = "Start";
  } else {
    timerToggleBtn.textContent = "Pause";
    timerInterval = setInterval(() => {
      if (timerSeconds > 0) {
        timerSeconds--;
        updateTimerDisplay();
      } else {
        clearInterval(timerInterval);
        timerInterval = null;
        timerToggleBtn.textContent = "Start";
        alert("Well done! Your 1-hour study block is complete!");
      }
    }, 1000);
  }
}

function resetTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  timerSeconds = 3600;
  timerToggleBtn.textContent = "Start";
  updateTimerDisplay();
}

// State helpers (localStorage)
function loadProgress() {
  // Check if any state exists
  if (!localStorage.getItem("netacademy-weeks-completed")) {
    localStorage.setItem("netacademy-weeks-completed", JSON.stringify([]));
  }
}

function getWeekCompletedState(idx) {
  const completed = JSON.parse(localStorage.getItem("netacademy-weeks-completed") || "[]");
  return completed.includes(idx);
}

function markWeekComplete(idx) {
  const completed = JSON.parse(localStorage.getItem("netacademy-weeks-completed") || "[]");
  if (!completed.includes(idx)) {
    completed.push(idx);
    localStorage.setItem("netacademy-weeks-completed", JSON.stringify(completed));
  }
  renderSidebar();
  updateOverallProgress();
}

function toggleWeekComplete(idx, e) {
  e.stopPropagation(); // Prevent trigger click navigation
  const completed = JSON.parse(localStorage.getItem("netacademy-weeks-completed") || "[]");
  const pos = completed.indexOf(idx);
  
  if (pos === -1) {
    completed.push(idx);
  } else {
    completed.splice(pos, 1);
  }
  
  localStorage.setItem("netacademy-weeks-completed", JSON.stringify(completed));
  renderSidebar();
  updateOverallProgress();
}

function updateOverallProgress() {
  const completed = JSON.parse(localStorage.getItem("netacademy-weeks-completed") || "[]");
  const percent = Math.round((completed.length / curriculum.length) * 100);
  overallProgressText.textContent = `${percent}%`;
  overallProgressBar.style.width = `${percent}%`;
}

// Run initializer
window.addEventListener("DOMContentLoaded", initApp);
