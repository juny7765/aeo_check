import React, { useState, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  SafeAreaView,
  StatusBar,
  Platform
} from 'react-native';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export default function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const reportRef = useRef(null); // Ref to capture for PDF

  const runAudit = async () => {
    if (!url.trim()) return;
    setLoading(true);
    setReport(null);

    // Determines API URL based on environment
    // If localhost, use port 8001. If production (Vercel), use relative path /api/audit
    // Note: For React Native Web, window.location is available.
    let apiUrl = '/api/audit';
    if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
      apiUrl = 'http://localhost:8001/api/audit';
    }

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setReport(data);
    } catch (error) {
      console.error(error);
      alert('Failed to analyze. Is the backend on port 8001?');
    } finally {
      setLoading(false);
    }
  };

  const exportReport = async () => {
    if (!report || Platform.OS !== 'web') {
      alert("PDF download is only available on Web for now.");
      return;
    }

    try {
      const input = document.body; // Capture the whole page for simplicity
      // Or better, target a specific div if we could ID it. 
      // In RN Web, refs often point to nested nodes. 
      // Let's safe-guard:
      if (!input) return;

      const canvas = await html2canvas(input, {
        scale: 2, // Better resolution
        useCORS: true, // Handle images from other domains if any
        logging: false
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
      const imgX = (pdfWidth - imgWidth * ratio) / 2;
      const imgY = 10;

      // PDF Height calculation for long pages handled simply here (one page fit or multi-page?)
      // For MVP, we'll try to fit or just use standard fit. 
      // A better approach for long reports is:
      const imgProps = pdf.getImageProperties(imgData);
      const pdfH = (imgProps.height * pdfWidth) / imgProps.width;

      // Single page long PDF (A4 is fixed, but let's just make it fit width)
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfH);

      // Filename Logic: URL + Date
      const dateStr = new Date().toISOString().split('T')[0];
      let hostname = "website";
      try {
        hostname = new URL(report.url).hostname.replace('www.', '');
      } catch (e) { }

      pdf.save(`${hostname}_${dateStr}.pdf`);

    } catch (error) {
      console.error(error);
      alert("Failed to generate PDF");
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <ScrollView contentContainerStyle={styles.scrollContent} ref={reportRef}>

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>AEO 검사 전문가 (v3.6)</Text>
          <Text style={styles.headerSubtitle}>Abel & 김부장 제공</Text>
        </View>

        {/* Input Section */}
        <View style={styles.card}>
          <Text style={styles.label}>Target Website URL (v3.6 Check)</Text>
          <TextInput
            style={styles.input}
            placeholder="e.g. https://www.career-roast.com"
            placeholderTextColor="#666"
            value={url}
            onChangeText={setUrl}
            autoCapitalize="none"
            keyboardType="url"
          />

          <TouchableOpacity
            style={styles.button}
            onPress={runAudit}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#FFF" />
            ) : (
              <Text style={styles.buttonText}>Run Diagnostic</Text>
            )}
          </TouchableOpacity>
        </View>

        {/* Result Section */}
        {report && (
          <View style={styles.resultContainer}>

            {/* Score Badge */}
            <View style={[styles.scoreCard, { borderColor: getScoreColor(report.score) }]}>
              <Text style={[styles.scoreLabel, { color: getScoreColor(report.score) }]}>AEO SCORE</Text>
              <Text style={styles.scoreValue}>{report.score}</Text>
            </View>

            <Text style={styles.sectionTitle}>10-Point Analysis Results</Text>

            <View style={styles.listContainer}>
              {report.results.map((item, index) => (
                <View key={index} style={styles.listItem}>
                  <Text style={styles.listIcon}>{item.icon}</Text>
                  <View style={{ flex: 1 }}>
                    <Text style={styles.listTitle}>{item.title}</Text>
                    <Text style={[styles.listStatus, { color: item.status === 'Pass' ? '#4CD964' : '#FF3B30' }]}>
                      {item.desc}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
            <ServiceRecommendation results={report.results} url={url} />
          </View>
        )}

        {/* Export Button */}
        {report && Platform.OS === 'web' && (
          <TouchableOpacity style={styles.exportButton} onPress={exportReport}>
            <Text style={styles.exportButtonText}>Download Report as PDF</Text>
          </TouchableOpacity>
        )}

      </ScrollView>
    </SafeAreaView>
  );
}

const PRICING_MAP = {
  "Structured Data (JSON-LD)": { name: "구조화 데이터 심기", price: 300000, desc: "AI가 이해할 수 있는 언어로 사이트를 번역해줍니다." },
  "Meta Description": { name: "AI 매혹 메타 설명 작성", price: 150000, desc: "클릭률을 높이는 최적의 요약문을 작성합니다." },
  "Open Graph Tags": { name: "SNS/AI 썸네일 최적화", price: 100000, desc: "카톡/슬랙 등 공유 시 이쁘게 나오도록 수정합니다." },
  "Header Hierarchy (H1/H2)": { name: "논리적 헤더 구조 수리", price: 200000, desc: "검색엔진이 좋아하는 글 구조로 재배치합니다." },
  "Content Volume": { name: "AI 학습용 콘텐츠 보강", price: 400000, desc: "AI가 인용하기 좋게 본문 내용을 보강합니다." },
  "Internal Linking": { name: "지식 연결 고리 설계", price: 250000, desc: "사이트 내 문서들을 촘촘하게 연결합니다." },
  "Image Alt Text": { name: "이미지 AI 설명 태그 배포", price: 150000, desc: "이미지를 검색엔진에게 설명해줍니다." },
  "Mobile Friendly": { name: "모바일 뷰포트 긴급 수리", price: 200000, desc: "모바일 화면 깨짐 현상을 해결합니다." },
  "Robots.txt": { name: "문지기(Robots) 설정", price: 100000, desc: "검색 로봇의 출입을 올바르게 제어합니다." },
  "Sitemap.xml": { name: "사이트지도 제작 및 등록", price: 100000, desc: "구글/네이버에 지도(Sitemap)를 제출합니다." },
};

function ServiceRecommendation({ results, url }) {
  const failedItems = results.filter(r => r.status !== 'Pass');
  const recommendations = failedItems.map(item => PRICING_MAP[item.title]).filter(Boolean);

  // Base package price
  const consultationPrice = 100000; // Basic Analysis Fee
  const repairTotal = recommendations.reduce((sum, item) => sum + item.price, 0);
  const totalEstimate = repairTotal + consultationPrice;

  if (recommendations.length === 0) {
    return (
      <View style={styles.serviceCard}>
        <Text style={styles.serviceTitle}>🎉 완벽합니다!</Text>
        <Text style={styles.serviceDesc}>
          발견된 치명적인 기술적 문제가 없습니다.{"\n"}
          이제 콘텐츠 마케팅에 집중하실 단계입니다.
        </Text>
        <View style={styles.priceRow}>
          <Text style={styles.priceLabel}>AEO 유지관리(월)</Text>
          <Text style={styles.priceValue}>₩100,000</Text>
        </View>
        <ContactButton url={url} subject="AEO 유지관리 문의" />
      </View>
    );
  }

  return (
    <View style={styles.serviceCard}>
      <Text style={styles.serviceTitle}>🛠 김부장의 긴급 처방전</Text>
      <Text style={styles.serviceDesc}>
        빨간불이 뜬 항목들을 방치하면 AI 검색에서 영원히 제외될 수 있습니다.
        당장 고쳐야 할 항목들에 대한 견적입니다.
      </Text>

      {/* Itemized List */}
      <View style={styles.invoiceContainer}>
        {recommendations.map((item, idx) => (
          <View key={idx} style={styles.invoiceRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.invoiceItemName}>{item.name}</Text>
              <Text style={styles.invoiceItemDesc}>{item.desc}</Text>
            </View>
            <Text style={styles.invoiceItemPrice}>₩{item.price.toLocaleString()}</Text>
          </View>
        ))}
        <View style={[styles.invoiceRow, { borderBottomWidth: 0, marginTop: 10 }]}>
          <Text style={styles.invoiceItemName}>기본 정밀 진단비</Text>
          <Text style={styles.invoiceItemPrice}>₩{consultationPrice.toLocaleString()}</Text>
        </View>
      </View>

      <View style={styles.priceRow}>
        <Text style={styles.priceLabel}>총 예상 견적</Text>
        <Text style={styles.priceValue}>₩{totalEstimate.toLocaleString()}</Text>
      </View>

      <ContactButton url={url} subject={`AEO 긴급 수리 견적(총 ${totalEstimate.toLocaleString()}원)`} />
    </View>
  );
}

function ContactButton({ url, subject }) {
  return (
    <TouchableOpacity
      style={styles.contactButton}
      onPress={() => {
        if (typeof window !== 'undefined') {
          window.open(`mailto:contact@abel.com?subject=${encodeURIComponent(subject)}&body=제 사이트 URL은 ${url} 입니다.`);
        }
      }}
    >
      <Text style={styles.contactButtonText}>전문가에게 해결 요청하기</Text>
    </TouchableOpacity>
  )
}

function getScoreColor(score) {
  if (score >= 80) return '#4CD964'; // Green
  if (score >= 50) return '#FFCC00'; // Yellow
  return '#FF3B30'; // Red
}

// ... existing styles ...

