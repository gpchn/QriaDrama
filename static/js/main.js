function run(drama) {
  // 跳转到阅读器页面，并传递剧本标题作为参数
  window.location.href = `reader.html?title=${encodeURIComponent(drama.title)}`;
}


// 页面加载完成后获取dramas数据
window.addEventListener("pywebviewready", function () {
  loadDramas();
});

// 加载dramas数据
function loadDramas() {
  pywebview.api.get_dramas().then((dramas) => {
    displayDramas(dramas);
  });
}

// 显示dramas数据
function displayDramas(dramas) {
  const dramasList = $("#dramas-list")
  dramasList.empty(); // 清空列表

  dramas.forEach((drama) => {
    // 创建drama元素
    const dramaElement = $("<div>");
    dramaElement.addClass("drama-item");

    // 设置背景图
    dramaElement.css("background-image", `url(${drama.cover})`);

    // 创建标题容器
    const titleContainer = $("<div>");
    titleContainer.addClass("drama-title-container");

    // 创建标题
    const titleElement = $("<h3>");
    titleElement.text(drama.title);
    titleElement.addClass("drama-title");

    // 添加点击事件
    dramaElement.on("click", function () {
      run(drama);
    });

    // 组装元素
    titleContainer.append(titleElement);
    dramaElement.append(titleContainer);
    dramasList.append(dramaElement);
  });
}

