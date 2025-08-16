/**
 * 跳转到剧本阅读器页面
 * @param {Object} drama - 剧本对象，包含标题等信息
 */
function run(drama) {
  window.location.href = `reader.html?title=${encodeURIComponent(drama.title)}`;
}

/**
 * 页面加载完成后初始化剧本列表
 */
window.addEventListener("pywebviewready", loadDramas);

/**
 * 从后端API获取剧本数据
 */
function loadDramas() {
  pywebview.api
    .get_dramas()
    .then(displayDramas)
    .catch((error) => {
      $("#dramas-list").html(
        "<div class='error-message'>加载剧本失败: " + error.message + "</div>"
      );
    });
}

/**
 * 在页面上显示剧本列表
 * @param {Array} dramas - 剧本数组
 */
function displayDramas(dramas) {
  const dramasList = $("#dramas-list").empty();

  if (!dramas || dramas.length === 0) {
    dramasList.append(
      "<div class='no-dramas-message'>没有找到可用的剧本</div>"
    );
    return;
  }

  dramas.forEach((drama) => {
    const dramaElement = createDramaElement(drama);
    dramasList.append(dramaElement);
  });
}

/**
 * 创建单个剧本元素
 * @param {Object} drama - 剧本对象
 * @returns {jQuery} 剧本元素
 */
function createDramaElement(drama) {
  const dramaElement = $("<div>").addClass("drama-item");

  // 设置背景图或默认背景
  if (drama.cover) {
    dramaElement.css("background-image", `url(${drama.cover})`);
  } else {
    dramaElement.css("background-color", "#2a1f29");
  }

  // 创建标题容器和标题
  const titleContainer = $("<div>").addClass("drama-title-container");
  const titleElement = $("<h3>").addClass("drama-title").text(drama.title);

  // 添加描述（如果有）
  if (drama.description) {
    const descContainer = $("<div>").addClass("drama-content-container");
    const descElement = $("<p>")
      .addClass("drama-description")
      .text(drama.description);
    descContainer.append(descElement);
    dramaElement.append(descContainer);
  }

  // 添加点击事件
  dramaElement.on("click", () => run(drama));

  // 组装元素
  titleContainer.append(titleElement);
  dramaElement.append(titleContainer);

  return dramaElement;
}
