package com.makemathgreatagain

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import java.nio.charset.StandardCharsets

private const val PREFS = "math_learning"
private const val MASTERED_TOPICS = "mastered_topics"
private const val API_BASE_URL_PREF = "api_base_url"
private const val DEFAULT_API_BASE_URL = "http://10.0.2.2:8000"

private val MmgaColors = lightColorScheme(
    primary = Color(0xFF315CA8),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFE7EEF9),
    onPrimaryContainer = Color(0xFF173765),
    secondary = Color(0xFF17756B),
    secondaryContainer = Color(0xFFE1F3EF),
    tertiary = Color(0xFF9A5B10),
    tertiaryContainer = Color(0xFFFFE9C2),
    background = Color(0xFFF5F6F8),
    surface = Color.White,
    surfaceVariant = Color(0xFFE7EAF0),
    onSurface = Color(0xFF1D2430),
    onSurfaceVariant = Color(0xFF5C6472),
    outline = Color(0xFFD6DAE2),
    error = Color(0xFFB42318),
)

private val ScreenPadding = 18.dp
private val CardShape = RoundedCornerShape(8.dp)
private val PillShape = RoundedCornerShape(999.dp)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent { MmgaApp() }
    }
}

private data class Topic(
    val id: String,
    val name: String,
    val gradeBand: String,
    val textbookPositions: List<TextbookPosition>,
    val human: String,
    val lifeExamples: List<String>,
    val why: String,
    val formalDefinition: String,
    val prerequisites: List<String>,
    val next: List<String>,
    val terms: Map<String, String>,
    val misconceptions: List<String>,
    val formulas: List<String>,
    val visuals: List<String>,
    val exerciseTypes: List<String>,
    val schoolRoute: List<String>,
    val route: List<String>,
)

private data class TextbookPosition(
    val curriculum: String,
    val grade: String,
    val chapter: String,
    val section: String,
)

private data class UiState(
    val loading: Boolean = true,
    val error: String? = null,
    val topics: List<Topic> = BuiltInTopics,
    val selected: Topic? = null,
    val mastered: Set<String> = emptySet(),
    val answer: String = "",
    val apiBaseUrl: String = DEFAULT_API_BASE_URL,
    val dataSource: String = "本机内置",
    val syncWarning: String? = null,
)

private data class GradeBucket(
    val key: String,
    val label: String,
    val topics: List<Topic>,
)

private enum class TopicFilter(val label: String) {
    All("全部"),
    Open("还没懂"),
    Mastered("已经懂"),
}

private enum class MainTab(val label: String) {
    School("校内"),
    Understand("理解"),
    Review("复习"),
    Settings("设置"),
}

@Composable
private fun MmgaApp() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var state by remember {
        mutableStateOf(
            UiState(
                loading = false,
                mastered = loadMastered(context),
                apiBaseUrl = loadApiBaseUrl(context),
            ),
        )
    }

    suspend fun loadTopics(baseUrl: String = state.apiBaseUrl) {
        val selectedId = state.selected?.id
        state = state.copy(loading = true, error = null)
        state = try {
            val topics = fetchTopics(baseUrl)
            state.copy(
                loading = false,
                topics = topics,
                selected = selectedId?.let { id -> topics.firstOrNull { it.id == id } },
                error = null,
                dataSource = "后端同步",
                syncWarning = null,
            )
        } catch (error: Exception) {
            state.copy(
                loading = false,
                topics = state.topics.ifEmpty { BuiltInTopics },
                selected = selectedId?.let { id ->
                    state.topics.firstOrNull { it.id == id }
                        ?: BuiltInTopics.firstOrNull { it.id == id }
                },
                error = null,
                dataSource = "本机内置",
                syncWarning = error.message ?: "后端暂时不可用",
            )
        }
    }

    LaunchedEffect(Unit) {
        loadTopics()
    }

    MaterialTheme(colorScheme = MmgaColors) {
        Surface(color = MaterialTheme.colorScheme.background) {
            AppScreen(
                state = state,
                onReload = { scope.launch { loadTopics() } },
                onSelect = { state = state.copy(selected = it, answer = "") },
                onBack = { state = state.copy(selected = null, answer = "") },
                onToggleMastered = { topic ->
                    val mastered = state.mastered.toMutableSet()
                    if (!mastered.add(topic.id)) mastered.remove(topic.id)
                    saveMastered(context, mastered)
                    state = state.copy(mastered = mastered)
                },
                onAsk = { topic, question ->
                    state = state.copy(answer = "AI 老师正在根据掌握记录回答")
                    state = try {
                        state.copy(
                            answer = fetchTeacherAnswer(
                                state.apiBaseUrl,
                                topic.id,
                                question,
                                state.mastered,
                            ),
                        )
                    } catch (_: Exception) {
                        state.copy(
                            answer = "AI 后端未连接。校内内容可以继续看；"
                                + "设置里填可访问的后端地址后再问。",
                        )
                    }
                },
                onSaveApiBaseUrl = { apiBaseUrl ->
                    val normalized = normalizeBaseUrl(apiBaseUrl)
                    saveApiBaseUrl(context, normalized)
                    state = state.copy(apiBaseUrl = normalized)
                    scope.launch { loadTopics(normalized) }
                },
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AppScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    onBack: () -> Unit,
    onToggleMastered: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    onSaveApiBaseUrl: (String) -> Unit,
) {
    var selectedTab by rememberSaveable { mutableStateOf(MainTab.School) }

    BackHandler(enabled = state.selected != null, onBack = onBack)
    BackHandler(enabled = state.selected == null && selectedTab != MainTab.School) {
        selectedTab = MainTab.School
    }

    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = { Text("MMGA", fontWeight = FontWeight.SemiBold) },
                navigationIcon = {
                    if (state.selected != null) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.Filled.ArrowBack, contentDescription = "返回")
                        }
                    }
                },
                actions = {
                    IconButton(onClick = onReload, enabled = !state.loading) {
                        Icon(Icons.Filled.Refresh, contentDescription = "刷新")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    navigationIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                ),
            )
        },
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 0.dp,
            ) {
                MainTab.entries.forEach { tab ->
                    NavigationBarItem(
                        selected = selectedTab == tab && state.selected == null,
                        onClick = {
                            if (state.selected != null) onBack()
                            selectedTab = tab
                        },
                        icon = { TabIcon(tab) },
                        label = { Text(tab.label) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant,
                        ),
                    )
                }
            }
        },
    ) { padding ->
        if (state.selected != null) {
            TopicDetail(
                topic = state.selected,
                topics = state.topics,
                mastered = state.mastered,
                answer = state.answer,
                onToggleMastered = onToggleMastered,
                onAsk = onAsk,
                modifier = Modifier.padding(padding),
            )
        } else {
            when (selectedTab) {
                MainTab.School -> SchoolRouteScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Understand -> UnderstandingRouteScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Review -> ReviewScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Settings -> SettingsScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    onSaveApiBaseUrl = onSaveApiBaseUrl,
                    modifier = Modifier.padding(padding),
                )
            }
        }
    }
}

@Composable
private fun TabIcon(tab: MainTab) {
    when (tab) {
        MainTab.School -> SchoolGlyph()
        MainTab.Understand -> RouteGlyph()
        MainTab.Review -> ReviewGlyph()
        MainTab.Settings -> SettingsGlyph()
    }
}

@Composable
private fun SchoolGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor),
        )
        Spacer(Modifier.height(3.dp))
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor.copy(alpha = 0.75f)),
        )
        Spacer(Modifier.height(3.dp))
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor.copy(alpha = 0.5f)),
        )
    }
}

@Composable
private fun RouteGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
        Box(
            modifier = Modifier
                .width(2.dp)
                .height(8.dp)
                .background(contentColor.copy(alpha = 0.65f)),
        )
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
    }
}

@Composable
private fun ReviewGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        repeat(3) {
            Box(
                modifier = Modifier
                    .padding(vertical = 2.dp)
                    .width(16.dp)
                    .height(2.dp)
                    .background(contentColor),
            )
        }
    }
}

@Composable
private fun SettingsGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(3.dp, Alignment.CenterVertically),
    ) {
        SliderGlyphRow(dotOnLeft = false, color = contentColor)
        SliderGlyphRow(dotOnLeft = true, color = contentColor)
        SliderGlyphRow(dotOnLeft = false, color = contentColor.copy(alpha = 0.75f))
    }
}

@Composable
private fun SliderGlyphRow(dotOnLeft: Boolean, color: Color) {
    Row(
        modifier = Modifier.width(18.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(3.dp),
    ) {
        if (dotOnLeft) {
            Box(Modifier.size(5.dp).clip(CircleShape).background(color))
        }
        Box(
            modifier = Modifier
                .weight(1f)
                .height(2.dp)
                .background(color.copy(alpha = 0.7f)),
        )
        if (!dotOnLeft) {
            Box(Modifier.size(5.dp).clip(CircleShape).background(color))
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SchoolRouteScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    var query by rememberSaveable { mutableStateOf("") }
    var filter by rememberSaveable { mutableStateOf(TopicFilter.All) }
    val orderedTopics = state.topics.schoolOrdered()
    val gradeBuckets = orderedTopics.gradeBuckets()
    val gradeKeys = gradeBuckets.joinToString("|") { it.key }
    var selectedGradeKey by rememberSaveable { mutableStateOf<String?>(null) }
    val selectedGrade = gradeBuckets.firstOrNull { it.key == selectedGradeKey }
        ?: gradeBuckets.firstOrNull()
    val searchText = query.trim()
    val sourceTopics = if (searchText.isBlank()) {
        selectedGrade?.topics.orEmpty()
    } else {
        orderedTopics
    }
    val stepNumbers = sourceTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()
    val filteredTopics = sourceTopics.filter { topic ->
        val matchesQuery = searchText.isBlank() ||
            listOf(topic.name, topic.schoolPlace(), topic.human).any {
                it.contains(searchText, ignoreCase = true)
            }
        val matchesFilter = when (filter) {
            TopicFilter.All -> true
            TopicFilter.Open -> topic.id !in state.mastered
            TopicFilter.Mastered -> topic.id in state.mastered
        }
        matchesQuery && matchesFilter
    }

    LaunchedEffect(gradeKeys) {
        val keys = gradeBuckets.map { it.key }
        if (keys.isNotEmpty() && (selectedGradeKey == null || selectedGradeKey !in keys)) {
            selectedGradeKey = gradeBuckets.first().key
        }
    }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            SchoolHomeHeader(
                selectedGrade = selectedGrade?.label ?: "年级",
                total = state.topics.size,
                mastered = state.mastered.size,
            )
        }
        item {
            GradeSelector(
                buckets = gradeBuckets,
                selectedKey = selectedGrade?.key,
                onSelect = { selectedGradeKey = it },
            )
        }
        item {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("搜全部课本，比如 分数、方程") },
                leadingIcon = {
                    Icon(Icons.Filled.Search, contentDescription = null)
                },
                shape = CardShape,
            )
        }
        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                TopicFilter.entries.forEach { option ->
                    FilterChip(
                        selected = filter == option,
                        onClick = { filter = option },
                        label = { Text(option.label) },
                    )
                }
            }
        }
        if (state.error != null) {
            item {
                ErrorPanel(message = state.error, onReload = onReload)
            }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) {
                LoadingTopicRow()
            }
        } else if (filteredTopics.isEmpty()) {
            item {
                EmptyPanel()
            }
        } else {
            items(filteredTopics, key = { it.id }) { topic ->
                CompactTopicRow(
                    step = stepNumbers.getValue(topic.id),
                    topic = topic,
                    mastered = topic.id in state.mastered,
                    primaryMeta = topic.schoolPlace(),
                    secondaryMeta = topic.human,
                ) {
                    onSelect(topic)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun UnderstandingRouteScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val orderedTopics = state.topics.understandingOrdered()
    val stepNumbers = orderedTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            RouteChoiceHeader(
                title = "按理解补：按先后顺序",
                body = "如果你不知道一个词到底是什么意思，走这条路。"
                    + "它先补更早需要懂的东西，再走到后面的正式说法。",
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else if (orderedTopics.isEmpty()) {
            item { EmptyPanel("暂无理解路线") }
        } else {
            item {
                SectionHeader(
                    title = "理解顺序",
                    meta = "${orderedTopics.count { it.id in state.mastered }}/${orderedTopics.size} 已经懂",
                )
            }
            items(orderedTopics, key = { "understand-${it.id}" }) { topic ->
                CompactTopicRow(
                    step = stepNumbers.getValue(topic.id),
                    topic = topic,
                    mastered = topic.id in state.mastered,
                    primaryMeta = topic.understandingPreview(),
                    secondaryMeta = "学校里通常在：${topic.schoolPlace()}",
                ) {
                    onSelect(topic)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun RouteChoiceHeader(
    title: String,
    body: String,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.primaryContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                title,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                fontSize = 20.sp,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                body,
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 14.sp,
                lineHeight = 21.sp,
            )
        }
    }
}

@Composable
private fun ReviewScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val knownIds = state.topics.map { it.id }.toSet()
    val orderedTopics = state.topics.understandingOrdered()
    val stepNumbers = orderedTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()
    val openTopics = orderedTopics.filter { it.id !in state.mastered }
    val readyTopics = openTopics.filter { topic ->
        topic.prerequisites
            .filter { prerequisite -> prerequisite in knownIds }
            .all { prerequisite -> prerequisite in state.mastered }
    }
    val nextTopics = (readyTopics.ifEmpty { openTopics }).take(1)
    val masteredTopics = orderedTopics.filter { it.id in state.mastered }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ProgressStrip(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else {
            item {
                SectionHeader(
                    title = "下一步",
                    meta = if (nextTopics.isEmpty()) {
                        "没有还没懂的知识"
                    } else {
                        "按理解顺序只给一个"
                    },
                )
            }
            if (nextTopics.isEmpty()) {
                item { EmptyPanel("暂无还没懂的知识") }
            } else {
                items(nextTopics, key = { "next-${it.id}" }) { topic ->
                    CompactTopicRow(
                        step = stepNumbers.getValue(topic.id),
                        topic = topic,
                        mastered = false,
                        primaryMeta = "下一步先学它",
                        secondaryMeta = topic.schoolPlace(),
                    ) {
                        onSelect(topic)
                    }
                }
            }

            item {
                SectionHeader(
                    title = "已经懂",
                    meta = "${masteredTopics.size} 个知识点",
                )
            }
            if (masteredTopics.isEmpty()) {
                item { EmptyPanel("还没有已经懂的记录") }
            } else {
                items(masteredTopics, key = { "review-${it.id}" }) { topic ->
                    CompactTopicRow(
                        step = stepNumbers.getValue(topic.id),
                        topic = topic,
                        mastered = true,
                        primaryMeta = "复习时先问自己：我能用自己的话说出来吗？",
                        secondaryMeta = topic.schoolPlace(),
                    ) {
                        onSelect(topic)
                    }
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun SettingsScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    onSaveApiBaseUrl: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var apiBaseUrl by rememberSaveable(state.apiBaseUrl) {
        mutableStateOf(state.apiBaseUrl)
    }
    val orderedTopics = state.topics.understandingOrdered()
    val openTopics = orderedTopics.filter { it.id !in state.mastered }
    val nextTopic = openTopics.firstOrNull()
    val weakNames = nextTopic
        ?.prerequisites
        ?.filter { it !in state.mastered }
        ?.names(state.topics)
        .orEmpty()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            SettingsHeader(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        item {
            DetailPanel(title = "AI 老师") {
                OutlinedTextField(
                    value = apiBaseUrl,
                    onValueChange = { apiBaseUrl = it },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    label = { Text("后端地址") },
                    shape = CardShape,
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                ) {
                    Button(
                        onClick = { onSaveApiBaseUrl(apiBaseUrl) },
                        enabled = normalizeBaseUrl(apiBaseUrl) != state.apiBaseUrl,
                        shape = CardShape,
                    ) {
                        Text("保存并同步")
                    }
                }
                SettingRow("学习记忆", "使用本机已掌握记录：${state.mastered.size} 个知识点")
                BodyText("问 AI 老师时，会把已会知识和可能薄弱的前置知识一起带上。")
                Button(
                    onClick = {
                        if (nextTopic != null) onSelect(nextTopic)
                    },
                    enabled = nextTopic != null,
                    shape = CardShape,
                ) {
                    Text("去问下一步知识")
                }
            }
        }
        item {
            DetailPanel(title = "个人知识地图") {
                SettingRow("已经懂", "${state.mastered.size} 个")
                SettingRow(
                    "还没懂",
                    "${(state.topics.size - state.mastered.size).coerceAtLeast(0)} 个",
                )
                SettingRow("下一步", nextTopic?.name ?: "暂无")
                SettingRow("可能先补", weakNames.ifBlank { "暂无" })
            }
        }
        item {
            DetailPanel(title = "内容范围") {
                SettingRow("内容来源", state.dataSource)
                SettingRow("当前可用", "${state.topics.size} 个知识点")
                SettingRow("覆盖方式", "按小学到初中主线、校内年级和理解依赖组织")
                if (state.syncWarning != null) {
                    BodyText("后端未同步，当前显示本机内容。")
                }
                BodyText(
                    "这不是完整教材章节点数量。"
                        + "后续需要继续按教材章、节、小节把骨架拆细。",
                )
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun SettingsHeader(
    total: Int,
    mastered: Int,
    loading: Boolean,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                "设置",
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 22.sp,
                fontWeight = FontWeight.SemiBold,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBlock(
                    label = if (loading) "同步中" else "知识点",
                    value = total.toString(),
                    modifier = Modifier.weight(1f),
                )
                MetricBlock(
                    label = "AI 记忆",
                    value = mastered.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.secondary,
                )
            }
        }
    }
}

@Composable
private fun SettingRow(
    label: String,
    value: String,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            label,
            modifier = Modifier.width(82.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 13.sp,
            lineHeight = 20.sp,
        )
        Text(
            value,
            modifier = Modifier.weight(1f),
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 15.sp,
            lineHeight = 22.sp,
        )
    }
}

@Composable
private fun SchoolHomeHeader(
    selectedGrade: String,
    total: Int,
    mastered: Int,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    "校内路线",
                    color = MaterialTheme.colorScheme.onSurface,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    "现在看：$selectedGrade",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            SmallTag("已懂 $mastered/$total")
        }
    }
}

@Composable
private fun GradeSelector(
    buckets: List<GradeBucket>,
    selectedKey: String?,
    onSelect: (String) -> Unit,
) {
    if (buckets.isEmpty()) return

    LazyRow(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        items(buckets, key = { it.key }) { bucket ->
            FilterChip(
                selected = bucket.key == selectedKey,
                onClick = { onSelect(bucket.key) },
                label = { Text("${bucket.label} ${bucket.topics.size}") },
            )
        }
    }
}

@Composable
private fun SectionHeader(
    title: String,
    meta: String,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 2.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom,
    ) {
        Text(
            title,
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 18.sp,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            meta,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ProgressStrip(
    total: Int,
    mastered: Int,
    loading: Boolean,
) {
    val open = (total - mastered).coerceAtLeast(0)
    val progress = if (total == 0) 0f else mastered.toFloat() / total.toFloat()

    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBlock(
                    label = if (loading) "同步中" else "全部",
                    value = total.toString(),
                    modifier = Modifier.weight(1f),
                )
                MetricBlock(
                    label = "已经懂",
                    value = mastered.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.secondary,
                )
                MetricBlock(
                    label = "还没懂",
                    value = open.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.tertiary,
                )
            }
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(PillShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(progress.coerceIn(0f, 1f))
                        .height(8.dp)
                        .background(MaterialTheme.colorScheme.primary),
                )
            }
        }
    }
}

@Composable
private fun MetricBlock(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
    valueColor: Color = MaterialTheme.colorScheme.onSurface,
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            label,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
        Text(value, color = valueColor, fontSize = 24.sp, fontWeight = FontWeight.SemiBold)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun CompactTopicRow(
    step: Int,
    topic: Topic,
    mastered: Boolean,
    primaryMeta: String,
    secondaryMeta: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier
                .clickable(onClick = onClick)
                .padding(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.Top,
        ) {
            Box(
                modifier = Modifier
                    .size(34.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    step.toString(),
                    color = MaterialTheme.colorScheme.primary,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                )
            }
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Text(
                    topic.name.ifBlank { topic.id },
                    fontSize = 17.sp,
                    lineHeight = 22.sp,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    primaryMeta,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    lineHeight = 18.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    secondaryMeta,
                    color = MaterialTheme.colorScheme.primary,
                    fontSize = 13.sp,
                    lineHeight = 18.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            StatusPill(mastered = mastered)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicRow(
    topic: Topic,
    mastered: Boolean,
    primaryMeta: String,
    secondaryMeta: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier
                .clickable(onClick = onClick)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        primaryMeta,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp,
                        lineHeight = 20.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        secondaryMeta,
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 13.sp,
                        lineHeight = 19.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
                StatusPill(mastered = mastered)
            }
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                SmallTag(topic.stageLabel())
                SmallTag("学它之前：${topic.prerequisites.size}个")
                SmallTag("以后会用：${topic.next.size}个")
            }
        }
    }
}

@Composable
private fun StatusPill(mastered: Boolean) {
    val container = if (mastered) {
        MaterialTheme.colorScheme.secondaryContainer
    } else {
        MaterialTheme.colorScheme.tertiaryContainer
    }
    val content = if (mastered) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.tertiary
    val label = if (mastered) "已经懂" else "还没懂"

    Surface(
        shape = PillShape,
        color = container,
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(7.dp)
                    .clip(CircleShape)
                    .background(content),
            )
            Text(label, color = content, fontSize = 12.sp, fontWeight = FontWeight.Medium)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicDetail(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    answer: String,
    onToggleMastered: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var question by rememberSaveable(topic.id) { mutableStateOf("") }
    var asking by remember(topic.id) { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            DetailHeader(
                topic = topic,
                mastered = topic.id in mastered,
                onToggleMastered = { onToggleMastered(topic) },
            )
        }
        item {
            DetailPanel(title = "课本里在哪里") {
                BodyText(topic.schoolPlace())
            }
        }
        item {
            DetailPanel(title = "讲解") {
                ExplanationText(topic.explanationText())
            }
        }
        item {
            DetailPanel(title = "关键词") {
                if (topic.terms.isEmpty()) {
                    BodyText("暂无")
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        topic.terms.entries.forEach { entry ->
                            TermRow(term = entry.key, explanation = entry.value)
                        }
                    }
                }
            }
        }
        item {
            LearningMap(
                topic = topic,
                topics = topics,
                mastered = mastered,
            )
        }
        item {
            DetailPanel(title = "误区与练习") {
                DenseTextBlock("容易错在", topic.misconceptions.ifEmpty { topic.defaultMisconceptions() })
                DenseTextBlock("练习方式", topic.exerciseTypes.ifEmpty { topic.defaultPractice() })
                if (topic.visuals.isNotEmpty()) {
                    DenseTextBlock("辅助表示", topic.visuals)
                }
            }
        }
        item {
            DetailPanel(title = "问 AI 老师") {
                AIMemoryNote(topic = topic, topics = topics, mastered = mastered)
                OutlinedTextField(
                    value = question,
                    onValueChange = { question = it },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    label = { Text("卡住的词、步骤或题目") },
                    enabled = !asking,
                    shape = CardShape,
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                ) {
                    Button(
                        onClick = {
                            val submitted = question.trim()
                            if (submitted.isNotEmpty()) {
                                scope.launch {
                                    asking = true
                                    onAsk(topic, submitted)
                                    asking = false
                                }
                            }
                        },
                        enabled = question.isNotBlank() && !asking,
                        shape = CardShape,
                    ) {
                        if (asking) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                color = MaterialTheme.colorScheme.onPrimary,
                                strokeWidth = 2.dp,
                            )
                            Spacer(Modifier.width(8.dp))
                        }
                        Text("问老师")
                    }
                }
                if (answer.isNotBlank()) {
                    AnswerBubble(answer = answer)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun AIMemoryNote(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
) {
    val known = topic.prerequisites.names(topics, onlyMastered = mastered)
    val weak = topic.prerequisites.names(topics, excludeMastered = mastered)

    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        SmallTag("会参考已懂记录：${mastered.size} 个")
        MapRow("本题前面已经会", known)
        MapRow("本题前面可能要补", weak)
    }
}

@Composable
private fun DetailHeader(
    topic: Topic,
    mastered: Boolean,
    onToggleMastered: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.Top,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 26.sp,
                        lineHeight = 32.sp,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        topic.human,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 15.sp,
                        lineHeight = 22.sp,
                    )
                }
                SmallTag(topic.stageLabel())
            }
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                StatusPill(mastered = mastered)
                Button(onClick = onToggleMastered, shape = CardShape) {
                    Text(if (mastered) "我还没懂" else "我懂了")
                }
            }
        }
    }
}

@Composable
private fun LearningMap(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
) {
    DetailPanel(title = "学它前后要知道什么") {
        MapRow("已经会的旧知识", topic.prerequisites.names(topics, onlyMastered = mastered))
        MapRow("可能要先补的旧知识", topic.prerequisites.names(topics, excludeMastered = mastered))
        MapRow("以后会用到它的知识", topic.next.names(topics))
    }
}

@Composable
private fun RouteLine(
    label: String,
    steps: List<String>,
) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(label, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        BodyText(steps.joinToString(" -> "))
    }
}

@Composable
private fun DetailPanel(
    title: String,
    content: @Composable ColumnScope.() -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                title,
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
            )
            content()
        }
    }
}

@Composable
private fun MapRow(label: String, value: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(value, fontSize = 15.sp, lineHeight = 22.sp, color = MaterialTheme.colorScheme.onSurface)
    }
}

@Composable
private fun DenseTextBlock(
    label: String,
    values: List<String>,
) {
    if (values.isEmpty()) return

    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontSize = 13.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        BodyText(values.joinToString("；") + "。")
    }
}

@Composable
private fun ExplanationText(value: String) {
    BodyText(value)
}

@Composable
private fun TermRow(term: String, explanation: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(term, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        BodyText(explanation)
    }
}

@Composable
private fun RouteStep(index: Int, value: String) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Box(
            modifier = Modifier
                .size(28.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center,
        ) {
            Text(index.toString(), color = MaterialTheme.colorScheme.primary, fontSize = 12.sp)
        }
        BodyText(value, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun AnswerBubble(answer: String) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.secondaryContainer,
    ) {
        Text(
            answer,
            modifier = Modifier.padding(14.dp),
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 15.sp,
            lineHeight = 23.sp,
        )
    }
}

@Composable
private fun BodyText(
    value: String,
    modifier: Modifier = Modifier,
) {
    Text(
        value,
        modifier = modifier,
        color = MaterialTheme.colorScheme.onSurface,
        fontSize = 15.sp,
        lineHeight = 23.sp,
    )
}

@Composable
private fun SmallTag(value: String) {
    Surface(
        shape = PillShape,
        color = MaterialTheme.colorScheme.surfaceVariant,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            value,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ErrorPanel(
    message: String,
    onReload: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = Color(0xFFFFF1F0),
        border = BorderStroke(1.dp, Color(0xFFFFDAD6)),
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("同步失败", color = Color(0xFFB42318), fontWeight = FontWeight.SemiBold)
                Text(message, color = Color(0xFF8C1D18), fontSize = 13.sp, maxLines = 2)
            }
            Button(onClick = onReload, shape = CardShape) {
                Text("重试")
            }
        }
    }
}

@Composable
private fun EmptyPanel(message: String = "没有匹配结果") {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            message,
            modifier = Modifier.padding(18.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun LoadingTopicRow() {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            LoadingBar(width = 0.42f, height = 18.dp)
            LoadingBar(width = 0.88f, height = 14.dp)
            LoadingBar(width = 0.55f, height = 14.dp)
        }
    }
}

@Composable
private fun LoadingBar(width: Float, height: androidx.compose.ui.unit.Dp) {
    Box(
        modifier = Modifier
            .fillMaxWidth(width)
            .height(height)
            .clip(PillShape)
            .background(MaterialTheme.colorScheme.surfaceVariant),
    )
}

private fun List<String>.names(
    topics: List<Topic>,
    onlyMastered: Set<String>? = null,
    excludeMastered: Set<String>? = null,
): String {
    val names = filter {
        (onlyMastered == null || it in onlyMastered) &&
            (excludeMastered == null || it !in excludeMastered)
    }.map { id -> topics.firstOrNull { it.id == id }?.name ?: id }
    return names.joinToString("、").ifBlank { "暂无" }
}

private fun Topic.stageLabel(): String = when (gradeBand) {
    "primary" -> "小学会学"
    "junior" -> "初中会学"
    "primary_to_junior" -> "小初衔接会用"
    else -> gradeBand.ifBlank { "校内知识" }
}

private fun Topic.schoolPlace(): String {
    val position = textbookPositions.firstOrNull()
    if (position != null) {
        return listOf(position.grade, position.chapter, position.section)
            .filter { it.isNotBlank() }
            .joinToString(" · ")
            .ifBlank { stageLabel() }
    }
    return schoolRoute.joinToString(" · ").ifBlank { stageLabel() }
}

private fun Topic.understandingPreview(): String {
    val steps = route.take(4)
    return if (steps.isEmpty()) {
        "入口：" + human.ifBlank { name }
    } else {
        "顺序：${steps.joinToString(" -> ")}"
    }
}

private fun Topic.explanationText(): String {
    val paragraphs = mutableListOf<String>()
    if (human.isNotBlank()) {
        paragraphs += human
    }
    if (why.isNotBlank()) {
        paragraphs += why
    }
    if (lifeExamples.isNotEmpty()) {
        paragraphs += "可以把它放到这些场景里看：${lifeExamples.joinToString("、")}。"
    }
    if (route.isNotEmpty()) {
        paragraphs += "理解顺序是：${route.joinToString("，然后")}。"
    }
    val definition = formalDefinition.ifBlank { human }
    if (definition.isNotBlank() && definition != human) {
        paragraphs += "课本里的正式说法是：$definition"
    }
    if (formulas.isNotEmpty()) {
        paragraphs += "常见写法：${formulas.joinToString("，")}。"
    }
    return paragraphs.joinToString("\n\n").ifBlank { "暂无讲解" }
}

private fun Topic.defaultMisconceptions(): List<String> = listOf(
    "只记住说法或公式，但说不出它表示什么。",
    "能做熟题，换一种问法就不知道该怎样判断。",
)

private fun Topic.defaultPractice(): List<String> = listOf(
    "用自己的话讲一遍这个知识点。",
    "举一个例子，并说清楚例子里的数量或图形关系。",
    "做题前先说清楚已知什么、要求什么、该用哪个关系。",
)

private fun List<Topic>.schoolOrdered(): List<Topic> = mapIndexed { index, topic -> index to topic }
    .sortedWith(
        compareBy<Pair<Int, Topic>> { it.second.textbookPositions.firstOrNull()?.grade.gradeOrder() }
            .thenBy { it.second.textbookPositions.firstOrNull()?.chapter.chapterOrder() }
            .thenBy { it.first },
    )
    .map { it.second }

private fun List<Topic>.gradeBuckets(): List<GradeBucket> {
    val order = listOf(
        "一年级",
        "二年级",
        "三年级",
        "四年级",
        "五年级",
        "六年级",
        "七年级",
        "八年级",
        "九年级",
        "小学",
        "初中",
        "其他",
    )
    val grouped = groupBy { it.schoolGradeKey() }
    return order.mapNotNull { key ->
        grouped[key]?.let { topics ->
            GradeBucket(key = key, label = key, topics = topics)
        }
    }
}

private fun Topic.schoolGradeKey(): String {
    val value = textbookPositions.firstOrNull()?.grade.orEmpty()
    return when {
        "一年级" in value -> "一年级"
        "二年级" in value -> "二年级"
        "三年级" in value -> "三年级"
        "四年级" in value -> "四年级"
        "五年级" in value -> "五年级"
        "六年级" in value -> "六年级"
        "七年级" in value -> "七年级"
        "八年级" in value -> "八年级"
        "九年级" in value -> "九年级"
        gradeBand == "primary" -> "小学"
        gradeBand == "junior" -> "初中"
        else -> "其他"
    }
}

private fun List<Topic>.understandingOrdered(): List<Topic> {
    val schoolOrder = schoolOrdered()
    val byId = schoolOrder.associateBy { it.id }
    val unresolved = schoolOrder.associate { it.id to it.prerequisites.count { id -> id in byId } }
        .toMutableMap()
    val dependents = mutableMapOf<String, MutableList<String>>()
    schoolOrder.forEach { topic ->
        topic.prerequisites.filter { it in byId }.forEach { prerequisite ->
            dependents.getOrPut(prerequisite) { mutableListOf() }.add(topic.id)
        }
    }
    val queue = schoolOrder.filter { unresolved[it.id] == 0 }.map { it.id }.toMutableList()
    val result = mutableListOf<Topic>()
    while (queue.isNotEmpty()) {
        val id = queue.removeAt(0)
        val topic = byId[id] ?: continue
        if (result.any { it.id == id }) continue
        result += topic
        dependents[id].orEmpty().forEach { nextId ->
            val nextCount = (unresolved[nextId] ?: 0) - 1
            unresolved[nextId] = nextCount
            if (nextCount == 0) queue += nextId
        }
    }
    if (result.size == schoolOrder.size) return result
    val seen = result.map { it.id }.toSet()
    return result + schoolOrder.filter { it.id !in seen }
}

private fun String?.gradeOrder(): Int {
    val value = this.orEmpty()
    val grade = when {
        "一年级" in value -> 1
        "二年级" in value -> 2
        "三年级" in value -> 3
        "四年级" in value -> 4
        "五年级" in value -> 5
        "六年级" in value -> 6
        "七年级" in value -> 7
        "八年级" in value -> 8
        "九年级" in value -> 9
        "小学" in value -> 3
        "初中" in value -> 7
        else -> 99
    }
    val volume = when {
        "上册" in value -> 0
        "下册" in value -> 1
        else -> 0
    }
    return grade * 10 + volume
}

private fun String?.chapterOrder(): Int {
    val value = this.orEmpty()
    val chineseDigits = mapOf(
        '一' to 1,
        '二' to 2,
        '三' to 3,
        '四' to 4,
        '五' to 5,
        '六' to 6,
        '七' to 7,
        '八' to 8,
        '九' to 9,
        '十' to 10,
    )
    Regex("""第(\d+)章""").find(value)?.groupValues?.get(1)?.toIntOrNull()?.let { return it }
    Regex("""第([一二三四五六七八九十]+)章""").find(value)?.groupValues?.get(1)?.let { text ->
        if (text == "十") return 10
        if (text.length == 1) return chineseDigits[text.first()] ?: 99
        if (text.startsWith("十")) return 10 + (chineseDigits[text.last()] ?: 0)
        if (text.endsWith("十")) return (chineseDigits[text.first()] ?: 0) * 10
        return (chineseDigits[text.first()] ?: 0) * 10 + (chineseDigits[text.last()] ?: 0)
    }
    return 99
}

private val BuiltInTopics = listOf(
    builtInTopic(
        id = "number_recognition",
        name = "数的认识",
        gradeBand = "primary",
        grade = "一年级上册",
        chapter = "数一数",
        section = "数表示多少",
        human = "数是用来回答“有多少”的工具。",
        why = "后面所有计算、测量和比较都要先知道数表示什么。",
        terms = mapOf("数" to "表示多少的记号。", "计数" to "一个一个对应着数出来。"),
        next = listOf("number_comparison", "place_value_decimal_system"),
        route = listOf("一个物体对应一个数", "数的顺序", "多少", "数字记号"),
        examples = listOf("数铅笔", "数台阶"),
        visuals = listOf("实物计数", "点子图"),
    ),
    builtInTopic(
        id = "number_comparison",
        name = "数的大小比较",
        gradeBand = "primary",
        grade = "一年级上册至二年级下册",
        chapter = "数的认识",
        section = "比较多少与大小",
        human = "比较大小是在判断两个数量谁多、谁少。",
        why = "估算、排序、分数小数比较和不等式都要先会比较。",
        terms = mapOf("大于" to "比另一个数多。", "小于" to "比另一个数少。"),
        prerequisites = listOf("number_recognition"),
        next = listOf("place_value_decimal_system"),
        route = listOf("一一对应", "多少", "数轴位置", "大于小于符号"),
        examples = listOf("比较两盒彩笔谁多", "按身高排队"),
        visuals = listOf("点子图", "数轴"),
    ),
    builtInTopic(
        id = "place_value_decimal_system",
        name = "十进制与位值",
        gradeBand = "primary",
        grade = "一年级下册至四年级上册",
        chapter = "100以内数的认识 / 大数的认识",
        section = "数位与计数单位",
        human = "同一个数字放在不同位置，表示的大小不一样。",
        why = "多位数、小数、竖式计算都靠位值来保证不乱。",
        terms = mapOf("数位" to "数字所在的位置。", "计数单位" to "一、十、百这样的单位。"),
        prerequisites = listOf("number_comparison"),
        next = listOf("integer_addition_subtraction", "decimal"),
        route = listOf("一捆十个", "十个十是一百", "位置不同", "值不同"),
        examples = listOf("23里的2表示2个十", "305里的0表示十位没有"),
        visuals = listOf("数位表", "小棒捆扎"),
    ),
    builtInTopic(
        id = "integer_addition_subtraction",
        name = "整数加减法",
        gradeBand = "primary",
        grade = "一年级上册至三年级上册",
        chapter = "加法和减法",
        section = "进位、退位与竖式",
        human = "加法是在合起来，减法是在拿走或比较差多少。",
        why = "这是理解数量变化和后续四则混合运算的入口。",
        terms = mapOf("进位" to "某一位满十后换成高一位的一个。"),
        prerequisites = listOf("place_value_decimal_system"),
        next = listOf("multiplication_meaning", "division_meaning"),
        route = listOf("合并或拿走", "按位对齐", "满十进一", "不够退一"),
        examples = listOf("一共有多少本书", "还剩多少个苹果"),
        visuals = listOf("数轴", "计数器"),
    ),
    builtInTopic(
        id = "multiplication_meaning",
        name = "乘法的意义",
        gradeBand = "primary",
        grade = "二年级上册",
        chapter = "表内乘法",
        section = "乘法的初步认识",
        human = "乘法是在说几个相同的组一共有多少。",
        why = "面积、比例、函数里的倍数关系都从乘法意义长出来。",
        terms = mapOf("几个几" to "有几组，每组有同样多个。"),
        prerequisites = listOf("integer_addition_subtraction"),
        next = listOf("division_meaning", "area"),
        route = listOf("重复加法", "相同组", "几个几", "乘法式子"),
        examples = listOf("3盒彩笔，每盒6支", "4排座位，每排8个"),
        visuals = listOf("阵列图", "分组图"),
    ),
    builtInTopic(
        id = "division_meaning",
        name = "除法的意义",
        gradeBand = "primary",
        grade = "二年级下册",
        chapter = "表内除法",
        section = "平均分",
        human = "除法是在平均分，或者看一个数量里有几个同样的组。",
        why = "分数、比、比例和概率都需要理解平均分和每份多少。",
        terms = mapOf("平均分" to "每份一样多。", "商" to "除法算出的结果。"),
        prerequisites = listOf("multiplication_meaning"),
        next = listOf("fraction"),
        route = listOf("平均分", "每份多少", "有几个组", "除法式子"),
        examples = listOf("12颗糖平均分给4人", "18里面有几个3"),
        visuals = listOf("分物图", "线段图"),
    ),
    builtInTopic(
        id = "fraction",
        name = "分数",
        gradeBand = "primary",
        grade = "三年级至五年级",
        chapter = "分数的认识",
        section = "几分之一与几分之几",
        human = "分数表示把一个整体平均分后取其中几份。",
        why = "比例、百分数、概率和代数式都需要表达不是整数的量。",
        terms = mapOf(
            "单位1" to "这次被当作一个完整整体的东西。",
            "分母" to "整体被平均分成几份。",
        ),
        prerequisites = listOf("division_meaning"),
        next = listOf("ratio", "probability"),
        route = listOf("整体", "平均分", "取几份", "分数符号"),
        examples = listOf("半块蛋糕", "四分之三杯水"),
        visuals = listOf("面积模型", "数轴"),
    ),
    builtInTopic(
        id = "decimal",
        name = "小数",
        gradeBand = "primary",
        grade = "三年级下册至四年级下册",
        chapter = "小数的初步认识",
        section = "小数表示与大小比较",
        human = "小数是把1继续平均分成十分、百分、千分后写出来的数。",
        why = "测量、钱数、百分数和函数图像都经常使用小数。",
        terms = mapOf("小数点" to "整数部分和小数部分的分界。"),
        prerequisites = listOf("place_value_decimal_system", "division_meaning"),
        next = listOf("ratio"),
        route = listOf("单位1", "继续平均分", "十分位", "百分位", "小数点"),
        examples = listOf("1.5米", "3.25元"),
        visuals = listOf("数轴", "方格纸"),
    ),
    builtInTopic(
        id = "measurement_units",
        name = "常见量与单位",
        gradeBand = "primary",
        grade = "二年级上册至三年级上册",
        chapter = "长度单位 / 时、分、秒 / 质量单位",
        section = "单位认识与换算",
        human = "单位是在说明这个数到底数的是什么。",
        why = "没有单位，测量、面积、速度和应用题都会失去意义。",
        terms = mapOf("单位" to "约定好的测量标准。", "换算" to "用不同单位表示同一个量。"),
        prerequisites = listOf("number_recognition"),
        next = listOf("area", "volume"),
        route = listOf("量什么", "选单位", "读数", "换算", "检验是否合理"),
        examples = listOf("3米和3厘米不是一回事", "1小时等于60分钟"),
        visuals = listOf("尺子", "钟表"),
    ),
    builtInTopic(
        id = "area",
        name = "面积",
        gradeBand = "primary",
        grade = "三年级下册至五年级上册",
        chapter = "面积 / 多边形的面积",
        section = "长方形、三角形和梯形面积",
        human = "面积是在问一个平面图形里面铺了多少个单位小方格。",
        why = "面积模型能解释乘法、几何公式和二次函数直觉。",
        terms = mapOf("面积单位" to "用来铺满平面的单位小方格。"),
        prerequisites = listOf("measurement_units", "multiplication_meaning"),
        next = listOf("volume"),
        route = listOf("铺方格", "数方格", "长乘宽", "割补转化", "公式"),
        examples = listOf("铺地砖", "计算土地大小"),
        visuals = listOf("方格纸", "割补图"),
    ),
    builtInTopic(
        id = "volume",
        name = "体积",
        gradeBand = "primary",
        grade = "五年级下册",
        chapter = "长方体和正方体",
        section = "体积和容积",
        human = "体积是在问一个立体里面能装多少个单位小正方体。",
        why = "空间想象、单位换算和初中几何都需要体积直觉。",
        terms = mapOf("体积单位" to "用来填满空间的小正方体。"),
        prerequisites = listOf("area"),
        next = listOf("coordinate_plane"),
        route = listOf("一层方格", "很多层", "长宽高", "单位小正方体", "体积公式"),
        examples = listOf("盒子能装多少", "水箱容量"),
        visuals = listOf("积木模型", "展开图"),
    ),
    builtInTopic(
        id = "ratio",
        name = "比",
        gradeBand = "primary",
        grade = "六年级上册",
        chapter = "比",
        section = "比的意义",
        human = "比是在比较两个数量之间的倍数关系。",
        why = "比例、相似、三角函数和函数斜率都离不开比。",
        terms = mapOf("比值" to "两个量相除得到的数。"),
        prerequisites = listOf("fraction", "decimal"),
        next = listOf("proportion"),
        route = listOf("两个量", "谁和谁比", "除法", "比值", "等价的比"),
        examples = listOf("果汁和水的配比", "地图比例尺"),
        visuals = listOf("线段图", "双数轴"),
    ),
    builtInTopic(
        id = "proportion",
        name = "比例",
        gradeBand = "primary",
        grade = "六年级下册",
        chapter = "比例",
        section = "正比例、反比例和比例尺",
        human = "比例是在说两个比相等，或者两个量按稳定规则一起变。",
        why = "一次函数、反比例函数、相似图形和建模都需要比例直觉。",
        terms = mapOf("正比例" to "一个量变成几倍，另一个量也变成几倍。"),
        prerequisites = listOf("ratio"),
        next = listOf("function_intro"),
        route = listOf("比", "两个比相等", "变化关系", "正比例", "反比例"),
        examples = listOf("速度一定时路程和时间", "总量一定时每份和份数"),
        visuals = listOf("表格", "双数轴"),
    ),
    builtInTopic(
        id = "equality",
        name = "等式",
        gradeBand = "primary",
        grade = "小学四年级",
        chapter = "简易方程准备",
        section = "等量关系",
        human = "等式就是两边表示同样多，像天平保持平衡。",
        why = "方程和代数推理都要依赖两边保持相等这个想法。",
        terms = mapOf("等号" to "表示左右两边一样多的符号。"),
        next = listOf("quantity_relationship", "transposition"),
        route = listOf("同样多", "两边平衡", "等号", "等式"),
        examples = listOf("两袋苹果一样重", "5元加3元和8元一样多"),
        visuals = listOf("天平模型", "左右数量条"),
    ),
    builtInTopic(
        id = "quantity_relationship",
        name = "数量关系",
        gradeBand = "primary_to_junior",
        grade = "小学高年级至初一",
        chapter = "式与方程",
        section = "用字母表示数",
        human = "数量关系是在说两个或多个数量怎样互相影响。",
        why = "函数、方程和应用题建模都从发现数量关系开始。",
        terms = mapOf("变量" to "会变化的数量。", "关系" to "几个数量互相影响的方式。"),
        prerequisites = listOf("equality"),
        next = listOf("linear_equation_one_variable", "function_intro"),
        route = listOf("生活变化", "两个量", "影响关系", "表达关系"),
        examples = listOf("路程会随着时间增加", "总价会随着数量增加"),
        visuals = listOf("关系表", "箭头图"),
    ),
    builtInTopic(
        id = "transposition",
        name = "移项",
        gradeBand = "junior",
        grade = "七年级上册",
        chapter = "第三章 一元一次方程",
        section = "解一元一次方程",
        human = "移项不是把数随便搬家，而是在等式两边做同样操作后的简写。",
        why = "解方程时要把含未知数的项和常数项整理到合适的位置。",
        terms = mapOf("项" to "式子里用加号或减号分开的每一块。"),
        prerequisites = listOf("equality"),
        next = listOf("linear_equation_one_variable"),
        route = listOf("等式平衡", "两边同操作", "整理未知数", "移项简写"),
        examples = listOf("天平两边同时拿走同样重的砝码"),
        visuals = listOf("天平变形", "左右式子颜色标注"),
    ),
    builtInTopic(
        id = "linear_equation_one_variable",
        name = "一元一次方程",
        gradeBand = "junior",
        grade = "七年级上册",
        chapter = "第三章 一元一次方程",
        section = "方程与解法",
        human = "一元一次方程就是只有一个未知数，且未知数只出现一次方的等量关系。",
        why = "它是从算术问题进入代数建模的第一道门。",
        terms = mapOf(
            "未知数" to "现在不知道、需要求出来的数。",
            "方程" to "含有未知数的等式。",
        ),
        prerequisites = listOf("equality", "quantity_relationship", "transposition"),
        next = listOf("function_intro"),
        route = listOf("未知数", "等量关系", "列式", "等式变形", "求解"),
        examples = listOf("已知总价和单价，求买了多少件"),
        visuals = listOf("天平模型", "线段图"),
    ),
    builtInTopic(
        id = "coordinate_plane",
        name = "平面直角坐标系",
        gradeBand = "junior",
        grade = "七年级下册",
        chapter = "第七章 平面直角坐标系",
        section = "有序数对与坐标",
        human = "坐标系用两个数确定平面上一个点的位置。",
        why = "函数图像、几何变换和数据图都需要坐标语言。",
        terms = mapOf("横坐标" to "表示左右位置的数。", "纵坐标" to "表示上下位置的数。"),
        prerequisites = listOf("number_comparison"),
        next = listOf("function_intro"),
        route = listOf("一条数轴定位", "两条数轴", "横纵方向", "有序数对", "点的位置"),
        examples = listOf("座位第3列第5排", "地图定位"),
        visuals = listOf("坐标纸", "地图网格"),
    ),
    builtInTopic(
        id = "function_intro",
        name = "函数入门",
        gradeBand = "junior",
        grade = "八年级下册",
        chapter = "第十九章 一次函数",
        section = "函数的概念",
        human = "函数是在描述一个量变了，另一个量怎样跟着变。",
        why = "函数把变化关系变成可以预测、画图和推理的数学对象。",
        terms = mapOf("输入" to "先给进去的那个数或条件。", "输出" to "根据输入得到的结果。"),
        prerequisites = listOf("quantity_relationship", "coordinate_plane"),
        next = listOf("probability"),
        route = listOf("生活变化", "两个量之间关系", "输入输出", "表格", "图像", "表达式"),
        examples = listOf("打车费用随里程变化", "水位随放水时间变化"),
        visuals = listOf("输入输出机器", "表格", "坐标图像"),
    ),
    builtInTopic(
        id = "probability",
        name = "概率初步",
        gradeBand = "junior",
        grade = "九年级上册",
        chapter = "第二十五章 概率初步",
        section = "随机事件、列举法和频率估计概率",
        human = "概率是在描述一件事发生的可能性有多大。",
        why = "它让学生用数量而不是感觉判断不确定事件。",
        terms = mapOf("随机事件" to "可能发生也可能不发生的事件。"),
        prerequisites = listOf("fraction"),
        route = listOf("可能或不可能", "所有结果", "有利结果", "比例", "频率估计"),
        examples = listOf("掷骰子", "抽签"),
        visuals = listOf("树状图", "列表"),
    ),
)

private fun builtInTopic(
    id: String,
    name: String,
    gradeBand: String,
    grade: String,
    chapter: String,
    section: String,
    human: String,
    why: String,
    terms: Map<String, String>,
    prerequisites: List<String> = emptyList(),
    next: List<String> = emptyList(),
    route: List<String> = emptyList(),
    examples: List<String> = emptyList(),
    visuals: List<String> = emptyList(),
): Topic = Topic(
    id = id,
    name = name,
    gradeBand = gradeBand,
    textbookPositions = listOf(
        TextbookPosition(
            curriculum = "本机内置数学主线",
            grade = grade,
            chapter = chapter,
            section = section,
        ),
    ),
    human = human,
    lifeExamples = examples,
    why = why,
    formalDefinition = human,
    prerequisites = prerequisites,
    next = next,
    terms = terms,
    misconceptions = emptyList(),
    formulas = emptyList(),
    visuals = visuals,
    exerciseTypes = emptyList(),
    schoolRoute = listOf(grade, chapter, section),
    route = route,
)

private suspend fun fetchTopics(baseUrl: String): List<Topic> = withContext(Dispatchers.IO) {
    val array = JSONArray(fetch(baseUrl, "/topics"))
    List(array.length()) { index -> array.getJSONObject(index).toTopic() }
}

private suspend fun fetchTeacherAnswer(
    baseUrl: String,
    topicId: String,
    question: String,
    mastered: Set<String>,
): String =
    withContext(Dispatchers.IO) {
        val query = URLEncoder.encode(question, StandardCharsets.UTF_8.name())
        val memory = URLEncoder.encode(
            mastered.sorted().joinToString(","),
            StandardCharsets.UTF_8.name(),
        )
        val path = "/topics/$topicId/teacher-answer?age=12&question=$query&mastered=$memory"
        JSONObject(fetch(baseUrl, path))
            .optString("answer")
    }

private fun JSONObject.toTopic(): Topic = Topic(
    id = optString("id"),
    name = optString("name"),
    gradeBand = optString("grade_band"),
    textbookPositions = optJSONArray("textbook_positions").toTextbookPositions(),
    human = optString("human_explanation"),
    lifeExamples = optJSONArray("life_examples").toStringList(),
    why = optString("why_needed"),
    formalDefinition = optString("formal_definition"),
    prerequisites = optJSONArray("prerequisite_ids").toStringList(),
    next = optJSONArray("next_ids").toStringList(),
    terms = optJSONObject("term_explanations").toStringMap(),
    misconceptions = optJSONArray("misconceptions").toStringList(),
    formulas = optJSONArray("formulas").toStringList(),
    visuals = optJSONArray("visualization_methods").toStringList(),
    exerciseTypes = optJSONArray("exercise_types").toStringList(),
    schoolRoute = optJSONArray("school_route").toStringList(),
    route = optJSONArray("understanding_route").toStringList(),
)

private fun JSONArray?.toTextbookPositions(): List<TextbookPosition> {
    if (this == null) return emptyList()
    return List(length()) { index ->
        val item = optJSONObject(index) ?: JSONObject()
        TextbookPosition(
            curriculum = item.optString("curriculum"),
            grade = item.optString("grade"),
            chapter = item.optString("chapter"),
            section = item.optString("section"),
        )
    }
}

private fun JSONArray?.toStringList(): List<String> {
    if (this == null) return emptyList()
    return List(length()) { index -> optString(index) }
}

private fun JSONObject?.toStringMap(): Map<String, String> {
    if (this == null) return emptyMap()
    return keys().asSequence().associateWith { key -> optString(key) }
}

private fun loadMastered(context: Context): Set<String> =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getStringSet(MASTERED_TOPICS, emptySet())
        .orEmpty()
        .toSet()

private fun saveMastered(context: Context, value: Set<String>) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putStringSet(MASTERED_TOPICS, value)
        .apply()
}

private fun loadApiBaseUrl(context: Context): String =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getString(API_BASE_URL_PREF, DEFAULT_API_BASE_URL)
        .orEmpty()
        .ifBlank { DEFAULT_API_BASE_URL }

private fun saveApiBaseUrl(context: Context, value: String) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putString(API_BASE_URL_PREF, value)
        .apply()
}

private fun normalizeBaseUrl(value: String): String =
    value.trim().trimEnd('/').ifBlank { DEFAULT_API_BASE_URL }

private fun fetch(baseUrl: String, path: String): String {
    val connection = URL(normalizeBaseUrl(baseUrl) + path).openConnection() as HttpURLConnection
    return try {
        connection.connectTimeout = 3000
        connection.readTimeout = 3000
        connection.requestMethod = "GET"
        if (connection.responseCode >= 400) error("HTTP ${connection.responseCode}")
        connection.inputStream.bufferedReader().use { it.readText() }
    } finally {
        connection.disconnect()
    }
}
