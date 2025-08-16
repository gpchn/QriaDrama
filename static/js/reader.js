// 全局变量
let currentDrama = null;
let currentLines = [];
let currentLineIndex = 0;
let currentDramaMeta = null;
let isTyping = false;
let typingSpeed = 50; // 打字速度（毫秒/字符）

// 页面加载完成后初始化
window.addEventListener("pywebviewready", function() {
    initializeReader();
});

// 初始化阅读器
function initializeReader() {
    // 获取URL参数中的剧本标题
    const urlParams = new URLSearchParams(window.location.search);
    const dramaTitle = urlParams.get('title');

    if (!dramaTitle) {
        console.error("未指定剧本标题");
        return;
    }

    // 添加开幕动画
    $("#reader-container").addClass("opening");

    // 确保开幕动画完成后再加载剧本
    setTimeout(function() {
        // 加载剧本数据
        loadDrama(dramaTitle);

        // 绑定事件
        bindEvents();
    }, 1000); // 等待开幕动画完成
}

// 加载剧本数据
function loadDrama(title) {
    pywebview.api.get_drama_lines(title).then(data => {
        if (!data) {
            console.error("无法加载剧本数据");
            return;
        }

        currentDrama = title;
        currentLines = data.lines;
        currentLineIndex = 0;
        currentDramaMeta = data.meta;

        // 显示第一行
        displayCurrentLine();
    });
}

// 显示当前行
function displayCurrentLine() {
    if (currentLineIndex >= currentLines.length) {
        // 剧本结束
        showEndMessage();
        return;
    }

    const line = currentLines[currentLineIndex];
    const characterName = Object.keys(line)[0];
    const dialogue = line[characterName];

    // 创建新的对话元素
    const $newDialogue = $('<div class="dialogue-item"></div>');

    // 添加角色名称
    const $newCharacterName = $(`<div class="character-name-item">${characterName}</div>`);

    // 设置角色颜色样式
    if (currentDramaMeta && currentDramaMeta.roles && currentDramaMeta.roles[characterName]) {
        $newCharacterName.attr("style", currentDramaMeta.roles[characterName]);
    } else {
        $newCharacterName.attr("style", "color: #FFDA79; text-shadow: 0 0 5px rgba(76, 23, 64, 0.5);");
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

// 打字机效果显示文本
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

// 显示下一行
function showNextLine() {
    if (isTyping) {
        // 如果正在打字，立即显示全部文本
        const $dialogueText = $("#dialogue-text");
        $dialogueText.text(currentLines[currentLineIndex][Object.keys(currentLines[currentLineIndex])[0]]);
        $dialogueText.removeClass("typing-cursor");
        // 移除了继续提示
        isTyping = false;
    } else {
        // 显示下一行
        currentLineIndex++;
        displayCurrentLine();
    }
}

// 显示剧本结束消息
function showEndMessage() {
    // 禁用所有键盘和鼠标事件
    $(document).off("keydown");
    $("#dialogue-box").off("click");

    // 创建"The End"元素
    const $theEnd = $('<div id="the-end">The End</div>');
    $("body").append($theEnd); // 添加到body而不是reader-container

    // 保持返回按钮可见
    $("#back-button").addClass("keep-visible");

    // 添加闭幕动画
    $("#reader-container").addClass("closing");

    // 动画结束后设置为关闭状态
    setTimeout(function() {
        $("#reader-container").addClass("closed");
        // 确保The End和返回按钮在动画结束后仍然可见
        $theEnd.addClass("visible");
        $("#back-button").addClass("keep-visible").css("z-index", "1001");
    }, 1800); // 与闭幕动画时间一致
}

// 更新进度指示器
function updateProgressIndicator() {
    const $progressIndicator = $("#progress-indicator");
    $progressIndicator.text(`${currentLineIndex + 1}/${currentLines.length}`);
}

// 绑定事件
function bindEvents() {
    // 返回按钮点击事件
    $("#back-button").on("click", function() {
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
}