<?php
	if (!empty($_GET['Name'])){
		$data = $_GET['Name'];
		$better_token = md5(uniqid(mt_rand(), true));
		move_uploaded_file($_FILES['file']['tmp_name'], "../../../not_approved_games/".$_FILES['file']['name'].$better_token.".py");
		echo json_encode("1");
	}
?>