/**
 * 跳转到剧本阅读器页面
 * @param {Object} drama - 剧本对象，包含标题等信息
 */
function run(drama) {
  console.log(`正在跳转到剧本阅读器: ${drama.title}`);
  // 跳转到阅读器页面，并传递剧本标题作为参数
  window.location.href = `reader.html?title=${encodeURIComponent(drama.title)}`;
}

/**
 * 页面加载完成后初始化剧本列表
 */
window.addEventListener("pywebviewready", function () {
  console.log("页面已准备就绪，开始加载剧本列表");
  loadDramas();
});

/**
 * 从后端API获取剧本数据
 */
function loadDramas() {
  console.log("正在从后端获取剧本数据...");
  pywebview.api.get_dramas().then((dramas) => {
    console.log(`成功获取到 ${dramas ? dramas.length : 0} 个剧本`);
    displayDramas(dramas);
  }).catch(error => {
    console.error("获取剧本数据失败:", error);
  });
}

/**
 * 在页面上显示剧本列表
 * @param {Array} dramas - 剧本数组
 */
function displayDramas(dramas) {
  console.log("开始渲染剧本列表");
  const dramasList = $("#dramas-list");
  dramasList.empty(); // 清空列表

  // 如果没有剧本数据，显示提示信息
  if (!dramas || dramas.length === 0) {
    console.warn("没有可显示的剧本数据");
    dramasList.append("<div class='no-dramas-message'>没有找到可用的剧本</div>");
    return;
  }

  dramas.forEach((drama, index) => {
    console.log(`正在渲染剧本 ${index + 1}/${dramas.length}: ${drama.title}`);

    // 创建drama元素
    const dramaElement = $("<div>");
    dramaElement.addClass("drama-item");

    // 设置背景图，如果没有则使用默认背景
    if (drama.cover) {
      dramaElement.css("background-image", `url(${drama.cover})`);
    } else {
      console.warn(`剧本 ${drama.title} 没有封面图片`);
      dramaElement.css("background-color", "#2a1f29");
    }

    // 创建标题容器
    const titleContainer = $("<div>");
    titleContainer.addClass("drama-title-container");

    // 创建标题
    const titleElement = $("<h3>");
    titleElement.text(drama.title);
    titleElement.addClass("drama-title");

    // 如果有描述，添加描述元素
    if (drama.description) {
      const descContainer = $("<div>");
      descContainer.addClass("drama-content-container");

      const descElement = $("<p>");
      descElement.text(drama.description);
      descElement.addClass("drama-description");

      descContainer.append(descElement);
      dramaElement.append(descContainer);
    }

    // 添加点击事件
    dramaElement.on("click", function () {
      console.log(`用户点击了剧本: ${drama.title}`);
      run(drama);
    });

    // 组装元素
    titleContainer.append(titleElement);
    dramaElement.append(titleContainer);
    dramasList.append(dramaElement);
  });

  console.log("剧本列表渲染完成");
}

