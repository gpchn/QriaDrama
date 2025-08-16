/**
 * 阅读器全局状态变量
 * 这些变量在整个阅读器生命周期中保持状态，用于跟踪当前阅读进度和状态
 */
let currentDrama = null;          // 当前加载的剧本标题
let currentLines = [];           // 当前剧本的所有对话行
let currentLineIndex = 0;        // 当前显示的对话行索引
let currentDramaMeta = null;     // 当前剧本的元数据（角色信息等）
let isTyping = false;            // 是否正在显示打字机效果
let typingSpeed = 50;            // 打字机效果的显示速度（毫秒/字符）

/**
 * 页面加载完成后初始化阅读器
 * 
 * 监听pywebviewready事件，该事件在Python后端与前端JavaScript桥接就绪后触发
 * 此时可以安全地调用后端API并初始化阅读器界面
 */
window.addEventListener("pywebviewready", initializeReader);

/**
 * 初始化阅读器
 * 
 * 执行阅读器的初始化操作，包括：
 * 1. 从URL获取剧本标题
 * 2. 应用开幕动画
 * 3. 加载剧本数据
 * 4. 绑定用户交互事件
 */
function initializeReader() {
  // 获取URL参数中的剧本标题
  const urlParams = new URLSearchParams(window.location.search);
  const dramaTitle = urlParams.get("title");

  // 检查是否获取到剧本标题
  if (!dramaTitle) {
    // 如果没有获取到剧本标题，显示错误信息
    $("#dialogue-text").html(
      "<div class='error-message'>错误：未指定剧本标题</div>"
    );
    return;
  }

  // 添加开幕动画类，触发CSS动画效果
  $("#reader-container").addClass("opening");

  // 确保开幕动画完成后再加载剧本
  // 使用setTimeout延迟加载，给动画足够时间展示
  setTimeout(() => {
    // 加载指定标题的剧本数据
    loadDrama(dramaTitle);
    // 绑定用户交互事件
    bindEvents();
  }, 1000);
}

/**
 * 从后端API加载剧本数据
 * 
 * 调用Python后端的get_drama_lines方法获取指定剧本的台词数据和元数据，
 * 成功后初始化状态并显示第一行对话，失败则显示错误信息
 * 
 * @param {string} title - 剧本标题，对应数据目录下的子目录名
 */
function loadDrama(title) {
  // 调用后端API获取剧本数据
  pywebview.api
    .get_drama_lines(title)
    .then((data) => {
      // 检查是否成功获取到数据
      if (!data) {
        // 如果没有获取到数据，显示错误信息
        $("#dialogue-text").html(
          `<div class='error-message'>错误：无法加载剧本 "${title}"</div>`
        );
        return;
      }

      // 初始化剧本数据
      currentDrama = title;                    // 设置当前剧本标题
      currentLines = data.lines || [];        // 设置对话行数组，如果没有则为空数组
      currentLineIndex = 0;                   // 重置当前行索引为0
      currentDramaMeta = data.meta || {};     // 设置剧本元数据，如果没有则为空对象

      // 显示第一行对话
      displayCurrentLine();
    })
    .catch((error) => {
      // 捕获并处理可能的错误
      $("#dialogue-text").html(
        `<div class='error-message'>加载剧本时发生错误: ${
          error.message || "未知错误"
        }</div>`
      );
    });
}

/**
 * 显示当前对话行
 * 
 * 根据当前行索引显示对应的对话内容，包括角色名称和对话文本，
 * 使用打字机效果显示文本，并更新进度指示器
 * 如果已到达剧本结尾，则显示结束消息
 */
function displayCurrentLine() {
  // 检查是否已到剧本结尾
  if (currentLineIndex >= currentLines.length) {
    // 如果已经显示完所有对话行，显示结束消息
    showEndMessage();
    return;
  }

  // 获取当前行数据
  const line = currentLines[currentLineIndex];
  // 获取角色名称（字典的键）
  const characterName = Object.keys(line)[0];
  // 获取对话内容（字典的值）
  const dialogue = line[characterName];

  // 创建对话元素（包含角色名称和对话文本）
  const dialogueElements = createDialogueElements(characterName, dialogue);

  // 获取对话框和对话文本区域的jQuery对象
  const $dialogueBox = $("#dialogue-box");
  const $dialogueText = $("#dialogue-text");

  // 移除现有的完成指示器（如果有）
  $(".complete-indicator").remove();

  // 永远不清空对话框内容，保留所有对话历史
  // 仅确保自动滚动到最新内容

  // 即使是第一行也不清空对话框，保留所有历史对话内容

  // 添加新对话到对话框
  $dialogueText.append(dialogueElements.container);

  // 使用打字机效果显示对话文本
  typeText(dialogue, dialogueElements.textElement);

  // 滚动到最新对话，确保用户可以看到最新内容
  $dialogueBox.scrollTop($dialogueBox[0].scrollHeight);

  // 更新进度指示器，显示当前行数和总行数
  updateProgressIndicator();
}

/**
 * 创建对话元素
 * 
 * 为单条对话创建HTML元素，包括角色名称和对话文本，
 * 根据剧本元数据中的角色样式设置角色名称的颜色和样式
 * 
 * @param {string} characterName - 角色名称
 * @param {string} dialogue - 对话内容
 * @returns {Object} 包含容器和文本元素的对象
 */
function createDialogueElements(characterName, dialogue) {
  // 创建新的对话项容器
  const $newDialogue = $('<div class="dialogue-item"></div>');

  // 添加角色名称元素
  const $newCharacterName = $(
    `<div class="character-name-item">${characterName}</div>`
  );

  // 设置角色颜色样式
  if (
    currentDramaMeta &&           // 确保有剧本元数据
    currentDramaMeta.roles &&     // 确保有角色信息
    currentDramaMeta.roles[characterName]  // 确保有当前角色的样式定义
  ) {
    // 如果有自定义角色样式，应用该样式
    $newCharacterName.attr("style", currentDramaMeta.roles[characterName]);
  } else {
    // 如果没有自定义样式，使用默认样式
    $newCharacterName.attr(
      "style",
      "color: #FFDA79; text-shadow: 0 0 5px rgba(76, 23, 64, 0.5);"
    );
  }

  // 添加对话文本元素
  const $newDialogueText = $('<div class="dialogue-text-item"></div>');

  // 组装新对话元素：将角色名称和对话文本添加到对话项容器
  $newDialogue.append($newCharacterName);
  $newDialogue.append($newDialogueText);

  // 返回创建的元素，供其他函数使用
  return {
    container: $newDialogue,      // 对话项容器
    textElement: $newDialogueText,  // 对话文本元素
  };
}

/**
 * 打字机效果显示文本
 * 
 * 逐个字符显示文本，模拟打字机效果，完成后添加完成指示器
 * 
 * @param {string} text - 要显示的文本
 * @param {jQuery} $element - 要显示文本的jQuery元素
 */
function typeText(text, $element) {
  // 设置打字状态为进行中
  isTyping = true;
  // 添加打字光标样式
  $element.addClass("typing-cursor");
  // 初始化字符索引
  let index = 0;

  // 创建定时器，逐个字符显示文本
  const timer = setInterval(() => {
    if (index < text.length) {
      // 如果还有字符未显示，显示下一个字符
      $element.text(text.substring(0, index + 1));
      index++;
    } else {
      // 如果所有字符都已显示，清除定时器
      clearInterval(timer);
      // 设置打字状态为已完成
      isTyping = false;
      // 移除打字光标样式
      $element.removeClass("typing-cursor");

      // 添加输出完毕的浮动指示器（向下箭头）
      const $completeIndicator = $('<span class="complete-indicator">▼</span>');
      $element.append($completeIndicator);

      // 添加跳动动画，提示用户可以继续
      setTimeout(() => {
        $completeIndicator.addClass("bounce-animation");
      }, 100);
    }
  }, typingSpeed);  // 使用预设的打字速度
}

/**
 * 显示下一行对话或立即完成当前打字效果
 * 
 * 根据当前状态决定是立即显示当前对话的全部内容，
 * 还是显示下一行对话
 */
function showNextLine() {
  if (isTyping) {
    // 如果正在显示打字效果，立即显示全部文本
    // 获取当前对话行的数据
    const line = currentLines[currentLineIndex];
    const characterName = Object.keys(line)[0];
    const dialogue = line[characterName];

    // 获取当前对话文本元素
    const $currentDialogue = $(
      "#dialogue-text .dialogue-item:last .dialogue-text-item"
    );
    // 立即显示全部文本
    $currentDialogue.text(dialogue);
    // 移除打字光标样式
    $currentDialogue.removeClass("typing-cursor");

    // 添加完成指示器
    const $completeIndicator = $('<span class="complete-indicator">▼</span>');
    $currentDialogue.append($completeIndicator);
    // 添加跳动动画
    setTimeout(() => {
      $completeIndicator.addClass("bounce-animation");
    }, 100);

    // 设置打字状态为已完成
    isTyping = false;
  } else {
    // 如果没有在显示打字效果，显示下一行对话
    // 增加行索引
    currentLineIndex++;
    // 显示新的对话行
    displayCurrentLine();
  }
}

/**
 * 显示剧本结束消息和动画
 * 
 * 当剧本阅读完成时，显示"The End"消息和返回按钮，
 * 并应用闭幕动画效果
 */
function showEndMessage() {
  // 禁用所有键盘和鼠标事件，防止用户继续交互
  $(document).off("keydown");
  $("#dialogue-box").off("click");

  // 创建"The End"元素
  const $theEnd = $('<div id="the-end">The End</div>');
  $("body").append($theEnd);

  // 添加新的返回按钮，放在The End下方
  const $newBackButton = $('<button id="end-back-button">返回主页</button>');
  $("body").append($newBackButton);

  // 添加闭幕动画类，触发CSS动画效果
  $("#reader-container").addClass("closing");

  // 动画结束后设置为关闭状态
  setTimeout(() => {
    // 添加关闭状态类
    $("#reader-container").addClass("closed");
    // 确保The End和新的返回按钮在动画结束后可见
    $theEnd.addClass("visible");
    $newBackButton.addClass("visible");

    // 为新的返回按钮绑定点击事件，点击时返回主页
    $newBackButton.on("click", () => {
      window.location.href = "index.html";
    });
  }, 1800);  // 等待闭幕动画完成
}

/**
 * 更新进度指示器
 * 
 * 更新页面上的进度指示器，显示当前行数和总行数
 */
function updateProgressIndicator() {
  // 设置进度指示器文本为"当前行数/总行数"格式
  $("#progress-indicator").text(
    `${currentLineIndex + 1}/${currentLines.length}`
  );
}

/**
 * 绑定用户交互事件
 * 
 * 为页面元素绑定各种用户交互事件，包括：
 * - 返回按钮点击事件
 * - 键盘按键事件
 * - 对话框点击事件
 */
function bindEvents() {
  // 返回按钮点击事件，点击时返回主页
  $("#back-button").on("click", () => {
    window.location.href = "index.html";
  });

  // 键盘事件监听
  $(document).on("keydown", (e) => {
    // 空格键、回车键显示下一行
    if (e.code === "Space" || e.code === "Enter") {
      // 阻止默认行为（如空格键滚动页面）
      e.preventDefault();
      // 显示下一行对话或完成当前打字效果
      showNextLine();
    }
  });

  // 点击对话框区域显示下一行
  $("#dialogue-box").on("click", showNextLine);
}
