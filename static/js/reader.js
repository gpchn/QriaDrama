/**
 * 阅读器全局状态变量
 */
// 当前加载的剧本标题
let currentDrama = null;
// 当前剧本的所有对话行
let currentLines = [];
// 当前显示的对话行索引
let currentLineIndex = 0;
// 当前剧本的元数据（包含角色样式等信息）
let currentDramaMeta = null;
// 打字机效果是否正在进行中
let isTyping = false;
// 打字速度（毫秒/字符）
let typingSpeed = 50;

/**
 * 页面加载完成后初始化阅读器
 */
window.addEventListener("pywebviewready", function() {
    console.log("阅读器页面准备就绪，开始初始化");
    initializeReader();
});

/**
 * 初始化阅读器
 * 1. 从URL获取剧本标题
 * 2. 应用开幕动画
 * 3. 加载剧本数据
 * 4. 绑定用户交互事件
 */
function initializeReader() {
    console.log("开始初始化阅读器");

    // 获取URL参数中的剧本标题
    const urlParams = new URLSearchParams(window.location.search);
    const dramaTitle = urlParams.get('title');

    console.log(`从URL获取剧本标题: ${dramaTitle || "未找到标题"}`);

    if (!dramaTitle) {
        console.error("未指定剧本标题，无法加载剧本");
        // 显示错误提示
        $("#dialogue-text").html("<div class='error-message'>错误：未指定剧本标题</div>");
        return;
    }

    // 添加开幕动画
    console.log("应用开幕动画");
    $("#reader-container").addClass("opening");

    // 确保开幕动画完成后再加载剧本
    setTimeout(function() {
        console.log("开幕动画完成，开始加载剧本数据");
        // 加载剧本数据
        loadDrama(dramaTitle);

        // 绑定事件
        console.log("绑定用户交互事件");
        bindEvents();
    }, 1000); // 等待开幕动画完成
}

/**
 * 从后端API加载剧本数据
 * @param {string} title - 剧本标题
 */
function loadDrama(title) {
    console.log(`正在加载剧本: ${title}`);

    pywebview.api.get_drama_lines(title).then(data => {
        if (!data) {
            console.error(`无法加载剧本数据: ${title}`);
            // 显示错误提示
            $("#dialogue-text").html(`<div class='error-message'>错误：无法加载剧本 "${title}"</div>`);
            return;
        }

        console.log(`成功加载剧本 "${title}"，包含 ${data.lines ? data.lines.length : 0} 行对话`);

        // 初始化剧本数据
        currentDrama = title;
        currentLines = data.lines || [];
        currentLineIndex = 0;
        currentDramaMeta = data.meta || {};

        console.log("剧本元数据:", currentDramaMeta);

        // 显示第一行
        displayCurrentLine();
    }).catch(error => {
        console.error(`加载剧本 "${title}" 时发生错误:`, error);
        $("#dialogue-text").html(`<div class='error-message'>加载剧本时发生错误: ${error.message || "未知错误"}</div>`);
    });
}

/**
 * 显示当前对话行
 */
function displayCurrentLine() {
    console.log(`显示第 ${currentLineIndex + 1} 行对话`);

    // 检查是否已到剧本结尾
    if (currentLineIndex >= currentLines.length) {
        console.log("剧本已结束");
        // 剧本结束
        showEndMessage();
        return;
    }

    // 获取当前行数据
    const line = currentLines[currentLineIndex];
    const characterName = Object.keys(line)[0];
    const dialogue = line[characterName];

    console.log(`角色: ${characterName}, 台词: ${dialogue.substring(0, 20)}${dialogue.length > 20 ? "..." : ""}`);

    // 创建新的对话元素
    const $newDialogue = $('<div class="dialogue-item"></div>');

    // 添加角色名称
    const $newCharacterName = $(`<div class="character-name-item">${characterName}</div>`);

    // 设置角色颜色样式
    if (currentDramaMeta && currentDramaMeta.roles && currentDramaMeta.roles[characterName]) {
        $newCharacterName.attr("style", currentDramaMeta.roles[characterName]);
        console.log(`为角色 ${characterName} 应用自定义样式`);
    } else {
        $newCharacterName.attr("style", "color: #FFDA79; text-shadow: 0 0 5px rgba(76, 23, 64, 0.5);");
        console.log(`为角色 ${characterName} 应用默认样式`);
    }

    // 添加对话文本
    const $newDialogueText = $('<div class="dialogue-text-item"></div>');

    // 组装新对话元素
    $newDialogue.append($newCharacterName);
    $newDialogue.append($newDialogueText);

    // 添加到对话框
    const $dialogueBox = $("#dialogue-box");
    const $dialogueText = $("#dialogue-text");

    // 移除所有现有的完成指示器
    $('.complete-indicator').remove();

    // 检查是否需要清空对话框（当文本累积超出容器上边缘时）
    if ($dialogueText.length > 0 && $dialogueText[0].scrollHeight > $dialogueBox[0].clientHeight * 1.5) {
        console.log("对话框内容过多，清空历史对话");
        $dialogueText.empty();
    }

    // 如果是第一行，确保对话框为空
    if (currentLineIndex === 0) {
        $dialogueText.empty();
    }

    // 添加新对话
    $dialogueText.append($newDialogue);

    // 使用打字机效果显示对话
    typeText(dialogue, $newDialogueText);

    // 滚动到最新对话
    $dialogueBox.scrollTop($dialogueBox[0].scrollHeight);

    // 更新进度指示器
    updateProgressIndicator();
}

/**
 * 打字机效果显示文本
 * @param {string} text - 要显示的文本
 * @param {jQuery} $element - 要显示文本的jQuery元素
 */
function typeText(text, $element) {
    console.log(`开始打字机效果，文本长度: ${text.length} 字符`);
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
            console.log("打字机效果完成");

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
    console.log("用户请求显示下一行");

    if (isTyping) {
        // 如果正在打字，立即显示全部文本
        console.log("正在打字中，立即显示全部文本");
        const line = currentLines[currentLineIndex];
        const characterName = Object.keys(line)[0];
        const dialogue = line[characterName];

        // 获取当前对话元素
        const $currentDialogue = $("#dialogue-text .dialogue-item:last .dialogue-text-item");
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
    console.log("剧本结束，显示结束动画");

    // 禁用所有键盘和鼠标事件
    $(document).off("keydown");
    $("#dialogue-box").off("click");
    console.log("已禁用用户交互事件");

    // 创建"The End"元素
    const $theEnd = $('<div id="the-end">The End</div>');
    $("body").append($theEnd); // 添加到body而不是reader-container

    // 添加新的返回按钮，放在The End下方
    const $newBackButton = $('<button id="end-back-button">返回主页</button>');
    $("body").append($newBackButton); // 添加到body

    // 添加闭幕动画
    $("#reader-container").addClass("closing");
    console.log("应用闭幕动画");

    // 动画结束后设置为关闭状态
    setTimeout(function() {
        $("#reader-container").addClass("closed");
        // 确保The End和新的返回按钮在动画结束后可见
        $theEnd.addClass("visible");
        $newBackButton.addClass("visible");

        // 为新的返回按钮绑定点击事件
        $newBackButton.on("click", function() {
            console.log("用户点击新的返回按钮");
            window.location.href = "index.html";
        });

        console.log("闭幕动画完成，已设置为关闭状态，新的返回按钮已显示");
    }, 1800); // 与闭幕动画时间一致
}

/**
 * 更新进度指示器
 */
function updateProgressIndicator() {
    const $progressIndicator = $("#progress-indicator");
    $progressIndicator.text(`${currentLineIndex + 1}/${currentLines.length}`);
    console.log(`更新进度: ${currentLineIndex + 1}/${currentLines.length}`);
}

/**
 * 绑定用户交互事件
 */
function bindEvents() {
    console.log("开始绑定用户交互事件");

    // 返回按钮点击事件
    $("#back-button").on("click", function() {
        console.log("用户点击返回按钮");
        window.location.href = "index.html";
    });

    // 键盘事件
    $(document).on("keydown", function(e) {
        // 空格键、回车键或方向键右/下显示下一行
        if (e.code === "Space" || e.code === "Enter") {
            e.preventDefault();
            showNextLine();
        }
    });

    // 点击对话框区域显示下一行
    $("#dialogue-box").on("click", function() {
        showNextLine();
    });

    console.log("用户交互事件绑定完成");
}