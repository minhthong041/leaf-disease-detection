import React from "react";
import {
  Button,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Container,
  Box,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

function App() {
  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      {/* Tiêu đề trang */}
      <Typography
        variant="h4"
        component="h1"
        align="center"
        gutterBottom
        color="primary"
        fontWeight="bold"
      >
        Hệ Thống Chẩn Đoán Bệnh Lá Cây
      </Typography>

      {/* Thẻ hiển thị ảnh và kết quả */}
      <Card sx={{ mt: 3, boxShadow: 3 }}>
        <CardMedia
          component="img"
          height="250"
          // Bạn có thể thay bằng link ảnh một chiếc lá thật
          image="https://via.placeholder.com/400x250?text=Chua+co+anh+tai+len"
          alt="Ảnh lá cây"
        />
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Kết quả phân tích:
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Vui lòng tải lên một bức ảnh lá cây để hệ thống AI xử lý và đưa ra
            chẩn đoán.
          </Typography>
        </CardContent>
      </Card>

      {/* Khu vực nút bấm */}
      <Box sx={{ mt: 4, display: "flex", justifyContent: "center" }}>
        <Button
          variant="contained"
          color="success"
          size="large"
          startIcon={<CloudUploadIcon />}
        >
          Tải ảnh lá cây lên
        </Button>
      </Box>
    </Container>
  );
}

export default App;
