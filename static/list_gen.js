function cons(){
	for (var i=0; i < {{rep_num.list}}; i++){
		var newDeadline = document.createElement("div");
		newDeadline.className = "deadline";
		newDeadline.innerHTML = "XX:YY";

		var newSubject = document.createElement("div");
		newSubject.className = "sub-name";
		newSubject.innerHTML = "流体力学";

		var newFile = document.createElement("div");
		newFile.className = "file-path";
		newFile.innerHTML = "課題２";

		var newMainContent = document.createElement("div");
		newMainContent.className = "acc-btn";
		newMainContent.appendChild(newDeadline);
		newMainContent.appendChild(newSubject);
		newMainContent.appendChild(newFile);

		var newOpen = document.createElement("img");
		newOpen.className = "func";
		newOpen.src = "../static/open.svg";

		var newOpenContainer = document.createElement("a");
		newOpenContainer.className = "func-around";
		newOpenContainer.href = "file:///D:/Users/maple/OneDrive - keio.jp/★課題★/.temp/st2019.pdf"
		newOpenContainer.appendChild(newOpen);

		var newSend = document.createElement("img");
		newSend.className = "func";
		newSend.src = "../static/send.svg";

		var newSendContainer = document.createElement("a");
		newSendContainer.className = "func-around";
		newSendContainer.href = "#";
		newSendContainer.appendChild(newSend);

		var newRefresh = document.createElement("img");
		newRefresh.className = "func";
		newRefresh.src = "../static/refresh.svg";

		var newRefreshContainer = document.createElement("a");
		newRefreshContainer.className = "func-around";
		newRefreshContainer.href = "#";
		newRefreshContainer.appendChild(newRefresh);

		var newDelete = document.createElement("img");
		newDelete.className = "func";
		newDelete.src = "../static/delete.svg";

		var newDeleteContainer = document.createElement("a");
		newDeleteContainer.className = "func-around";
		newDeleteContainer.href = "#";
		newDeleteContainer.appendChild(newDelete);

		var newContent = document.createElement("div");
		newContent.className = "task-func";
		newContent.appendChild(newOpenContainer);
		newContent.appendChild(newSendContainer);
		newContent.appendChild(newRefreshContainer);
		newContent.appendChild(newDeleteContainer);

		var newSubContent = document.createElement("div");
		newSubContent.className = "acc-content";
		newSubContent.appendChild(newContent);

		var newTask = document.createElement("div")
		newTask.className = "acc-group";
		newTask.appendChild(newMainContent);
		newTask.appendChild(newSubContent);

		var board = document.getElementById("left_tasks");
		board.appendChild(newTask);
	}
}// JavaScript Document