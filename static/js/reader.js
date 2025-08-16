/**
 * 阅读器全局状态变量
 */
let currentDrama = null;
let currentLines = [];
let currentLineIndex = 0;
let currentDramaMeta = null;
let isTyping = false;
let typingSpeed = 50;

/**
 * 页面加载完成后初始化阅读器
 */
window.addEventListener("pywebviewready", initializeReader);

/**
 * 初始化阅读器
 * 1. 从URL获取剧本标题
 * 2. 应用开幕动画
 * 3. 加载剧本数据
 * 4. 绑定用户交互事件
 */
function initializeReader() {
  // 获取URL参数中的剧本标题
  const urlParams = new URLSearchParams(window.location.search);
  const dramaTitle = urlParams.get("title");

  if (!dramaTitle) {
    $("#dialogue-text").html(
      "<div class='error-message'>错误：未指定剧本标题</div>"
    );
    return;
  }

  // 添加开幕动画
  $("#reader-container").addClass("opening");

  // 确保开幕动画完成后再加载剧本
  setTimeout(() => {
    loadDrama(dramaTitle);
    bindEvents();
  }, 1000);
}

/**
 * 从后端API加载剧本数据
 * @param {string} title - 剧本标题
 */
function loadDrama(title) {
  pywebview.api
    .get_drama_lines(title)
    .then((data) => {
      if (!data) {
        $("#dialogue-text").html(
          `<div class='error-message'>错误：无法加载剧本 "${title}"</div>`
        );
        return;
      }

      // 初始化剧本数据
      currentDrama = title;
      currentLines = data.lines || [];
      currentLineIndex = 0;
      currentDramaMeta = data.meta || {};

      // 显示第一行
      displayCurrentLine();
    })
    .catch((error) => {
      $("#dialogue-text").html(
        `<div class='error-message'>加载剧本时发生错误: ${
          error.message || "未知错误"
        }</div>`
      );
    });
}

/**
 * 显示当前对话行
 */
function displayCurrentLine() {
  // 检查是否已到剧本结尾
  if (currentLineIndex >= currentLines.length) {
    showEndMessage();
    return;
  }

  // 获取当前行数据
  const line = currentLines[currentLineIndex];
  const characterName = Object.keys(line)[0];
  const dialogue = line[characterName];

  // 创建对话元素
  const dialogueElements = createDialogueElements(characterName, dialogue);

  // 添加到对话框
  const $dialogueBox = $("#dialogue-box");
  const $dialogueText = $("#dialogue-text");

  // 移除现有的完成指示器
  $(".complete-indicator").remove();

  // 永远不清空对话框内容，保留所有对话历史
  // 仅确保自动滚动到最新内容

  // 即使是第一行也不清空对话框，保留所有历史对话内容

  // 添加新对话
  $dialogueText.append(dialogueElements.container);

  // 使用打字机效果显示对话
  typeText(dialogue, dialogueElements.textElement);

  // 滚动到最新对话
  $dialogueBox.scrollTop($dialogueBox[0].scrollHeight);

  // 更新进度指示器
  updateProgressIndicator();
}

/**
 * 创建对话元素
 * @param {string} characterName - 角色名称
 * @param {string} dialogue - 对话内容
 * @returns {Object} 包含容器和文本元素的对象
 */
function createDialogueElements(characterName, dialogue) {
  // 创建新的对话元素
  const $newDialogue = $('<div class="dialogue-item"></div>');

  // 添加角色名称
  const $newCharacterName = $(
    `<div class="character-name-item">${characterName}</div>`
  );

  // 设置角色颜色样式
  if (
    currentDramaMeta &&
    currentDramaMeta.roles &&
    currentDramaMeta.roles[characterName]
  ) {
    $newCharacterName.attr("style", currentDramaMeta.roles[characterName]);
  } else {
    $newCharacterName.attr(
      "style",
      "color: #FFDA79; text-shadow: 0 0 5px rgba(76, 23, 64, 0.5);"
    );
  }

  // 添加对话文本
  const $newDialogueText = $('<div class="dialogue-text-item"></div>');

  // 组装新对话元素
  $newDialogue.append($newCharacterName);
  $newDialogue.append($newDialogueText);

  return {
    container: $newDialogue,
    textElement: $newDialogueText,
  };
}

/**
 * 打字机效果显示文本
 * @param {string} text - 要显示的文本
 * @param {jQuery} $element - 要显示文本的jQuery元素
 */
function typeText(text, $element) {
  isTyping = true;
  $element.addClass("typing-cursor");
  let index = 0;

  const timer = setInterval(() => {
    if (index < text.length) {
      $element.text(text.substring(0, index + 1));
      index++;
    } else {
      clearInterval(timer);
      isTyping = false;
      $element.removeClass("typing-cursor");

      // 添加输出完毕的浮动标志
      const $completeIndicator = $('<span class="complete-indicator">▼</span>');
      $element.append($completeIndicator);

      // 添加跳动动画
      setTimeout(() => {
        $completeIndicator.addClass("bounce-animation");
      }, 100);
    }
  }, typingSpeed);
}

/**
 * 显示下一行对话或立即完成当前打字效果
 */
function showNextLine() {
  if (isTyping) {
    // 如果正在打字，立即显示全部文本
    const line = currentLines[currentLineIndex];
    const characterName = Object.keys(line)[0];
    const dialogue = line[characterName];

    // 获取当前对话元素
    const $currentDialogue = $(
      "#dialogue-text .dialogue-item:last .dialogue-text-item"
    );
    $currentDialogue.text(dialogue);
    $currentDialogue.removeClass("typing-cursor");

    // 添加完成指示器
    const $completeIndicator = $('<span class="complete-indicator">▼</span>');
    $currentDialogue.append($completeIndicator);
    setTimeout(() => {
      $completeIndicator.addClass("bounce-animation");
    }, 100);

    isTyping = false;
  } else {
    // 显示下一行
    currentLineIndex++;
    displayCurrentLine();
  }
}

/**
 * 显示剧本结束消息和动画
 */
function showEndMessage() {
  // 禁用所有键盘和鼠标事件
  $(document).off("keydown");
  $("#dialogue-box").off("click");

  // 创建"The End"元素
  const $theEnd = $('<div id="the-end">The End</div>');
  $("body").append($theEnd);

  // 添加新的返回按钮，放在The End下方
  const $newBackButton = $('<button id="end-back-button">返回主页</button>');
  $("body").append($newBackButton);

  // 添加闭幕动画
  $("#reader-container").addClass("closing");

  // 动画结束后设置为关闭状态
  setTimeout(() => {
    $("#reader-container").addClass("closed");
    // 确保The End和新的返回按钮在动画结束后可见
    $theEnd.addClass("visible");
    $newBackButton.addClass("visible");

    // 为新的返回按钮绑定点击事件
    $newBackButton.on("click", () => {
      window.location.href = "index.html";
    });
  }, 1800);
}

/**
 * 更新进度指示器
 */
function updateProgressIndicator() {
  $("#progress-indicator").text(
    `${currentLineIndex + 1}/${currentLines.length}`
  );
}

/**
 * 绑定用户交互事件
 */
function bindEvents() {
  // 返回按钮点击事件
  $("#back-button").on("click", () => {
    window.location.href = "index.html";
  });

  // 键盘事件
  $(document).on("keydown", (e) => {
    // 空格键、回车键显示下一行
    if (e.code === "Space" || e.code === "Enter") {
      e.preventDefault();
      showNextLine();
    }
  });

  // 点击对话框区域显示下一行
  $("#dialogue-box").on("click", showNextLine);
}
