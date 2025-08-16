/**
 * 跳转到剧本阅读器页面
 * 
 * 当用户点击剧本卡片时调用此函数，将页面导航到阅读器页面，
 * 并通过URL参数传递剧本标题
 * 
 * @param {Object} drama - 剧本对象，包含标题等信息
 */
function run(drama) {
  // 构建阅读器页面URL，将剧本标题作为查询参数传递
  // 使用encodeURIComponent确保标题中的特殊字符被正确编码
  window.location.href = `reader.html?title=${encodeURIComponent(drama.title)}`;
}

/**
 * 页面加载完成后初始化剧本列表
 * 
 * 监听pywebviewready事件，该事件在Python后端与前端JavaScript桥接就绪后触发
 * 此时可以安全地调用后端API
 */
window.addEventListener("pywebviewready", loadDramas);

/**
 * 从后端API获取剧本数据
 * 
 * 调用Python后端的get_dramas方法获取所有可用剧本的数据，
 * 成功后调用displayDramas函数显示剧本列表，
 * 失败则在页面上显示错误信息
 */
function loadDramas() {
  // 调用后端API获取剧本数据
  pywebview.api
    .get_dramas()
    // 成功获取数据后，调用displayDramas函数显示剧本列表
    .then(displayDramas)
    // 捕获并处理可能的错误
    .catch((error) => {
      // 在剧本列表容器中显示错误消息
      $("#dramas-list").html(
        "<div class='error-message'>加载剧本失败: " + error.message + "</div>"
      );
    });
}

/**
 * 在页面上显示剧本列表
 * 
 * 接收从后端获取的剧本数据，为每个剧本创建卡片元素并添加到页面中
 * 如果没有剧本数据，则显示提示信息
 * 
 * @param {Array} dramas - 剧本数组，每个元素包含剧本标题、封面等信息
 */
function displayDramas(dramas) {
  // 获取剧本列表容器并清空现有内容
  const dramasList = $("#dramas-list").empty();

  // 检查是否有剧本数据
  if (!dramas || dramas.length === 0) {
    // 如果没有剧本数据，显示提示信息
    dramasList.append(
      "<div class='no-dramas-message'>没有找到可用的剧本</div>"
    );
    return;
  }

  // 遍历剧本数组，为每个剧本创建卡片元素
  dramas.forEach((drama) => {
    const dramaElement = createDramaElement(drama);
    dramasList.append(dramaElement);
  });
}

/**
 * 创建单个剧本元素
 * 
 * 为单个剧本创建卡片元素，包括背景图、标题和描述等信息，
 * 并添加点击事件处理
 * 
 * @param {Object} drama - 剧本对象，包含标题、封面、描述等信息
 * @returns {jQuery} 剧本元素，包含所有样式和事件的jQuery对象
 */
function createDramaElement(drama) {
  // 创建剧本卡片元素
  const dramaElement = $("<div>").addClass("drama-item");

  // 设置背景图或默认背景
  if (drama.cover) {
    // 如果有封面图片，设置为背景图
    dramaElement.css("background-image", `url(${drama.cover})`);
  } else {
    // 如果没有封面图片，使用默认背景色
    dramaElement.css("background-color", "#2a1f29");
  }

  // 创建标题容器和标题元素
  const titleContainer = $("<div>").addClass("drama-title-container");
  const titleElement = $("<h3>").addClass("drama-title").text(drama.title);

  // 添加描述（如果有）
  if (drama.description) {
    // 创建描述容器和描述元素
    const descContainer = $("<div>").addClass("drama-content-container");
    const descElement = $("<p>")
      .addClass("drama-description")
      .text(drama.description);
    // 将描述元素添加到描述容器
    descContainer.append(descElement);
    // 将描述容器添加到剧本卡片
    dramaElement.append(descContainer);
  }

  // 添加点击事件，点击时调用run函数跳转到阅读器页面
  dramaElement.on("click", () => run(drama));

  // 组装元素：将标题元素添加到标题容器，再将标题容器添加到剧本卡片
  titleContainer.append(titleElement);
  dramaElement.append(titleContainer);

  // 返回创建好的剧本卡片元素
  return dramaElement;
}
